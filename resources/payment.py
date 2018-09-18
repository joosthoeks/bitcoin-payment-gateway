

from flask_restful import abort, reqparse, Resource
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import datetime as dt


rpc_user = 'user'
rpc_pass = 'pass'
rpc_conn = AuthServiceProxy('http://%s:%s@127.0.0.1:8332' % (rpc_user, rpc_pass))

PAYMENTS = {'p0': {}}

def abort_if_payment_doesnt_exist(payment_id):
    if payment_id not in PAYMENTS:
        abort(404, message="Payment {} doesn't exist".format(payment_id))

# parser for POST / INSERT / new payment:
parser = reqparse.RequestParser()
parser.add_argument('mode', choices=('test', 'live'), required=True)
parser.add_argument('satoshi', type=int, required=True)
parser.add_argument('description')
parser.add_argument('redirect_url')
parser.add_argument('webhook_url')
parser.add_argument('order_id', type=int)
parser.add_argument('customer_id', type=int)
parser.add_argument('merchant_id', type=int)
parser.add_argument('metadata')

# parser for PUT / UPDATE / modify payment:
parser2 = reqparse.RequestParser()
parser2.add_argument('status', choices=('open', 'canceled', 'pending', 'expired', 'failed', 'paid'))
parser2.add_argument('description')
parser2.add_argument('redirect_url')
parser2.add_argument('webhook_url')
parser2.add_argument('order_id', type=int)
parser2.add_argument('customer_id', type=int)
parser2.add_argument('merchant_id', type=int)
parser2.add_argument('metadata')


class Payment(Resource):

    def get(self, payment_id):
        abort_if_payment_doesnt_exist(payment_id)
        return PAYMENTS[payment_id], 200

    def delete(self, payment_id):
        abort_if_payment_doesnt_exist(payment_id)
        del PAYMENTS[payment_id]
        return '{}', 204

    def put(self, payment_id):
        abort_if_payment_doesnt_exist(payment_id)
        args = parser2.parse_args()
        status = args['status']
        if status is not None:
            PAYMENTS[payment_id]['status'] = status
        description = args['description']
        if description is not None:
            PAYMENTS[payment_id]['description'] = description
        redirect_url = args['redirect_url']
        if redirect_url is not None:
            PAYMENTS[payment_id]['redirect_url'] = redirect_url
        webhook_url = args['webhook_url']
        if webhook_url is not None:
            PAYMENTS[payment_id]['webhook_url'] = webhook_url
        order_id = args['order_id']
        if order_id is not None:
            PAYMENTS[payment_id]['order_id'] = order_id
        customer_id = args['customer_id']
        if customer_id is not None:
            PAYMENTS[payment_id]['customer_id'] = customer_id
        merchant_id = args['merchant_id']
        if merchant_id is not None:
            PAYMENTS[payment_id]['merchant_id'] = merchant_id
        metadata = args['metadata']
        if metadata is not None:
            PAYMENTS[payment_id]['metadata'] = metadata
        dt_upd = dt.datetime.now()
        last_updated = dt.datetime.strftime(dt_upd, '%Y-%m-%d %H:%M:%S')
        PAYMENTS[payment_id]['last_updated'] = last_updated
        return PAYMENTS[payment_id], 201


class PaymentList(Resource):

    def get(self):
        return PAYMENTS, 200

    def post(self):
        payment_id = int(max(PAYMENTS.keys()).lstrip('p')) + 1
        payment_id = 'p%i' % payment_id
        args = parser.parse_args()
        mode = args['mode']
        status = 'open'
        bitcoin_address = rpc_conn.getnewaddress()
        satoshi = args['satoshi']
        bitcoin_uri = 'bitcoin:%s?amount=%s' % (bitcoin_address, (satoshi / 100000000))
        description = args['description']
        redirect_url = args['redirect_url']
        webhook_url = args['webhook_url']
        order_id = args['order_id']
        customer_id = args['customer_id']
        merchant_id = args['merchant_id']
        metadata = args['metadata']
        dt_now = dt.datetime.now()
        created = dt.datetime.strftime(dt_now, '%Y-%m-%d %H:%M:%S')
        dt_exp = dt_now + dt.timedelta(minutes=15)
        expires = dt.datetime.strftime(dt_exp, '%Y-%m-%d %H:%M:%S')
        dt_upd = dt.datetime.now()
        last_updated = dt.datetime.strftime(dt_upd, '%Y-%m-%d %H:%M:%S')
        PAYMENTS[payment_id] = {
                'id': payment_id,
                'mode': mode,
                'status': status,
                'bitcoin_address': bitcoin_address,
                'satoshi': satoshi,
                'bitcoin_uri': bitcoin_uri,
                'description': description,
                'redirect_url': redirect_url,
                'webhook_url': webhook_url,
                'order_id': order_id,
                'customer_id': customer_id,
                'merchant_id': merchant_id,
                'metadata': metadata,
                'created': created,
                'expires': expires,
                'last_updated': last_updated,
                }
        return PAYMENTS[payment_id], 201
