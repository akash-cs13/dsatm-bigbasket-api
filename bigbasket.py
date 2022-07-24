from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import os

class Bigbasket_api(webdriver.Chrome):
    def __init__(self):
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.headless = True
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        super(Bigbasket_api, self).__init__(service=Service('chromedriver'), options=chrome_options)
        self.implicitly_wait(10)

    def initialization(self):
        self.get('https://www.bigbasket.com')

    def exit(self):
        self.quit()

    def set_location(self, city = 'Bangalore', pincode = '560028'):
        self.find_element(by=By.CLASS_NAME, value='arrow-marker').click()
        self.find_element(by=By.CLASS_NAME, value='ui-select-match-text').click()
        self.find_element(by=By.CLASS_NAME, value='ui-select-search').send_keys(city, Keys.ENTER)
        self.find_element(by=By.ID, value='areaselect').send_keys(pincode)
        sleep(0.3)
        self.find_element(by=By.ID, value='areaselect').send_keys(Keys.ENTER)
        sleep(0.3)
        self.find_element(by=By.ID, value='areaselect').send_keys(Keys.ENTER)

    def search_for_product(self, product):
        self.find_element(by=By.ID, value='input').send_keys(product, Keys.ENTER)

        items = self.find_elements(by=By.CSS_SELECTOR, value='a[ng-bind="vm.selectedProduct.p_desc"]')
        packet_desc = self.find_elements(by=By.CSS_SELECTOR, value='span[ng-bind="vm.selectedProduct.pack_desc"]')
        weight = self.find_elements(by=By.CSS_SELECTOR, value='span[ng-bind="vm.selectedProduct.w"]')
        price = self.find_elements(by=By.CSS_SELECTOR, value='''span[ng-bind="vm.selectedProduct.sp.replace('.00', '')"]''')
        url = self.find_elements(by=By.CSS_SELECTOR, value='a[ng-bind="vm.selectedProduct.p_desc"]')
        #image = self.find_elements(by=By.CLASS_NAME, value='img-responsive')
        image = self.find_elements(by=By.CSS_SELECTOR, value='img[data-sizes="auto"]')

        return_list = []
        for i in range(0, len(items)):
            return_list.append((items[i].text, packet_desc[i].text, weight[i].text, price[i].text, url[i].get_attribute("href"), image[i].get_attribute("src")))

        return return_list




if __name__ == '__main__':
    inst = Bigbasket_api()
    print("Initializing api.................................")
    inst.initialization()
    print("Setting up location.....................")
    inst.set_location()
    print("Initialization is done!!!!!!!!!\n")


    labels = ['Apple', 'Banana', 'Coconut', 'Curd', 'Guava', 'Mango', 'Milk', 'Mosambi', 'Muskmelon', 'Onion', 'Orange', 'Papaya', 'Pomegranate', 'Potato', 'Tomato']
    #labels = ['Apple', 'Onion', 'Potato']

    json_write = {}

    for read_string in labels:
        product_list = inst.search_for_product(read_string)
        print("Fetching data for "+ read_string)

        temp_list = []
        for item, packet_desc, weight, price, url, img in product_list:
            temp_list.append({"item": item, "packet_description": packet_desc + weight, "price": price, "url": url, "img": img})


        json_write[read_string] = temp_list
        print('\n')


    inst.quit()
    f = open("Bigbasketapi.json", "w")
    f.write(json.dumps(json_write))
    f.close()












