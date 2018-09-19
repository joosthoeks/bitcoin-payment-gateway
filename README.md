# bitcoin-payment-gateway
Self-hosted full-node Bitcoin payment gateway REST API server.

## GET all payments
```
$ curl -X GET -v http://test/payments/v1/payment
```
## POST new payment
```
$ curl -X POST -v http://test/payments/v1/payment -d mode='test' -d satoshi=1000000
```
## GET payment
```
$ curl -X GET -v http://test/payments/v1/payment/p1
```
## DELETE payment
```
$ curl -X DELETE -v http://test/payments/v1/payment/p1
```
## PUT update payment
```
$ curl -X PUT -v http://test/payments/v1/payment/p1 -d status='pending'
```
