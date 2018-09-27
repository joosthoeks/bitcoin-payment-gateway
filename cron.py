#!/usr/bin/env python3


import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


rpc_user = 'user'
rpc_pass = 'pass'
rpc_conn = AuthServiceProxy('http://%s:%s@127.0.0.1:8332' % (rpc_user, rpc_pass))


def main():
    url = 'http://test/payments/v1/payment'
    endpoint = ''
    full_url = '%s%s' % (url, endpoint)
    r = requests.get(full_url)
    for k, v in r.json().items():
        if k == 'p0':
            continue
        if v['status'] == 'paid':
            continue
        endpoint = '/%s' % k
        full_url = '%s%s' % (url, endpoint)
        if v['status'] == 'open' or v['status'] == 'pending':
            btc = v['satoshi'] * 100000000
            paid = rpc_conn.getreceivedbyaddress(v['bitcoin_address'])
            if paid >= btc:
                r2 = requests.put(full_url, data={'status': 'paid'})
            else:
                r2 = requests.put(full_url, data={'status': 'pending'})


if __name__ == '__main__':
    main()

