from flask import Flask,request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import requests
import json
import pprint
import os

#
# Author: FrancoUcci
# Used for faborder.go
# 03-Jul-2018
#

app = Flask(__name__)
api = Api(app)

# bcUrl="http://123.201.13.80:6110"
bcUrl=os.getenv('BC_URL')
bcBase='{"channel":"aclprodorderer","chaincode":"faborder2","chaincodeVer":"v1",'

api_url_inv = bcUrl+"/bcsgw/rest/v1/transaction/invocation"
api_url_qry = bcUrl+"/bcsgw/rest/v1/transaction/query"

print ("Your Blockchain API is powering up, and getting ready to serve you ....")
print ("Invocation url is : "+api_url_inv)
print ("Query url is : "+api_url_inv)
print ("Your Blockchain API is now fully powered up.")


# ProductList
#   shows a list of all products
class OrderList(Resource):
    def get(self):
        query_json = bcBase+'"method":"queryAllOrders","args":["BANANA73681710"]}'
        resp = requests.post(api_url_qry, data=query_json,
                             headers={'Content-Type': 'application/json'}, )

        if resp.status_code != 200:
            raise ApiError('POST '.format(resp.status_code))

        #print(resp.content)
        myResultTotal = json.loads(resp.content)
        myResult = json.loads(myResultTotal['result'])
        myResDump= json.dumps(myResult)
        #print(myResult)
        newOrder=[]

        for index,value in enumerate(myResult):
            #print index, value['Key'],value['Record']['buyer'],value['Record']['shipment'],value['Record']['status'],value['Record']['owner']
            newOrder.append({ 'orderId':value['Key'],'buyer':value['Record']['buyer'],'shipment':value['Record']['shipment'],'status':value['Record']['status'],'owner':value['Record']['owner']})

        print newOrder

        return newOrder


# Create Order (buyer,shipment, status, owner)
#
class OrderCreate(Resource):

    def post(self, order_id):
        paramsHere = '"' + order_id + '","' + request.json['buyer']+ '","' + request.json['shipment']+ '","' + request.json['status'] + '","' + request.json['owner'] + '"'
        change_json = bcBase + '"method":"createOrder","args":[' + paramsHere + ']}'
        print(change_json)
        resp = requests.post(api_url_inv, data=change_json,
                             headers={'Content-Type': 'application/json'}, )
        if resp.status_code != 200:
            raise ApiError('POST '.format(resp.status_code))
        return resp.json()


# Ship Order
#
class OrderShip(Resource):

    def put(self, order_id):
        paramsHere = '"'+order_id+'","'+request.json['owner']+'","'+request.json['status']+'"'
        change_json= bcBase+'"method":"shipOrder","args":['+ paramsHere +']}'
        print(change_json)
        resp = requests.post(api_url_inv, data=change_json,
                             headers={'Content-Type': 'application/json'}, )
        if resp.status_code != 200:
            raise ApiError('POST '.format(resp.status_code))
        return resp.json()

# Receive Order
#
class OrderReceive(Resource):

    def put(self, order_id):
        paramsHere = '"'+order_id+'","'+request.json['owner']+'","'+request.json['status']+'"'
        change_json= bcBase+'"method":"receiveOrder","args":['+ paramsHere +']}'
        print(change_json)
        resp = requests.post(api_url_inv, data=change_json,
                             headers={'Content-Type': 'application/json'}, )
        if resp.status_code != 200:
            raise ApiError('POST '.format(resp.status_code))
        return resp.json()

#
#   shows an Order in Detail
class OrderInDetail(Resource):
    def get(self,order_id):
        history_json= bcBase+'"method":"queryOrder","args":["'+ order_id +'"]}'
        resp = requests.post(api_url_qry, data=history_json,
                             headers={'Content-Type': 'application/json'}, )
        if resp.status_code != 200:
            raise ApiError('POST '.format(resp.status_code))

        myResultTotal = json.loads(resp.content)
        myResult = json.loads(myResultTotal['result'])
        myResDump= json.dumps(myResult)
        newRecord=[]

        newRecord.append({ 'orderId':order_id, 'buyer':myResult['buyer'],'shipment':myResult['shipment'],'status':myResult['status'],'owner':myResult['owner']})

        newRecord2 = { "Order":newRecord }
        print newRecord2
        return newRecord2


#   shows a Record History
class OrderHistory(Resource):
    def get(self,order_id):
        history_json= bcBase+'"method":"getHistoryForRecord","args":["'+ order_id +'"]}'
        resp = requests.post(api_url_qry, data=history_json,
                             headers={'Content-Type': 'application/json'}, )
        if resp.status_code != 200:
            raise ApiError('POST '.format(resp.status_code))

        #print(resp.content)
        myResultTotal = json.loads(resp.content)
        myResult = json.loads(myResultTotal['result'])
        myResDump= json.dumps(myResult)
        newRecordHistory=[]
        for index,value in enumerate(myResult):
            #print index, order_id,value['Timestamp'],value['Value']['buyer'],value['Value']['shipment'],value['Value']['status'],value['Value']['owner']
            newRecordHistory.append({ 'orderId':order_id, 'timestamp':value['Timestamp'],'buyer':value['Value']['buyer'],'shipment':value['Value']['shipment'],'status':value['Value']['status'],'owner':value['Value']['owner']})

        newRecordHistory2 = { "OrderHistory":newRecordHistory }
        print newRecordHistory2
        return newRecordHistory2

## Actually setup the Api resource routing here
##
api.add_resource(OrderList, '/orders')
api.add_resource(OrderInDetail, '/orders/<string:order_id>')
api.add_resource(OrderHistory, '/orders/<string:order_id>/history')

api.add_resource(OrderShip, '/orders/<string:order_id>/ship')
api.add_resource(OrderReceive, '/orders/<string:order_id>/receive')
api.add_resource(OrderCreate, '/orders/<string:order_id>')


if __name__ == '__main__':
    print "Welcome to the World Friendly Blockchain APIs"
    app.run(host='0.0.0.0', port=5002, debug=True)
