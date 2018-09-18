#!/usr/bin/env python3


from flask import Flask
from flask_restful import Api
from resources.payment import Payment, PaymentList


app = Flask(__name__)
api = Api(app)

# resources for bitcoin payments:
api.add_resource(PaymentList, '/payments/v1/payment')
api.add_resource(Payment, '/payments/v1/payment/<payment_id>')


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
