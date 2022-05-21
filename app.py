from flask import Flask, jsonify
from bigbasket import Bigbasket_api
import sys
import logging

app = Flask(__name__)


bigbasket = Bigbasket_api()


@app.route('/')
def myfun():
    return 'DSATM   Final year project'



@app.route('/bigbasket/init/<string:city>/<string:pincode>')
def api2_init(city, pincode):
    bigbasket.initialization()
    bigbasket.set_location(city=city, pincode=pincode)
    return jsonify({"bigbasket-result": "Initialized"})

@app.route('/bigbasket/search/<string:product>')
def api2(product):

    mylist = bigbasket.search_for_product(product=product)
    temp_list = []
    for item, packet_desc, weight ,price, url in mylist:
        temp_list.append({"item": item, "packet_description": packet_desc, "weight": weight, "price": price, "url": url})
    return jsonify({"bigbasket-result": "Success", "product": temp_list})

@app.route('/bigbasket/quit')
def api2_quit():
    bigbasket.exit()
    return jsonify({"bigbasket-result": "Quit"})


if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run(debug=True)



