# using flask_restful
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import pymongo
import json
from bson import json_util

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['materialbuy']
mycol = mydb['sellerrange']
sellercol = mydb['sellercol']
buyercol = mydb['buyercol']

class SellerRange(Resource):

    def post(self):
        data = request.get_json()
        rating = data['rating']
        ran = data['range']

        user_input = {"rating":rating, "ran": ran}

        mycol.insert_one(user_input)

        return make_response(jsonify("Data inserted!"), 200)

    def get(self):
        data = [doc for doc in mycol.find()]

        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)


class Buyer(Resource):
    
    def post(self):
        data = request.get_json()

        pin = data['pin']
        level = data['level']

        for i in range(0, len(pin)):
            user_input = {"pin": pin[i], "level": level}
            sellercol.insert_one(user_input)
        return make_response(jsonify("Inserted Data!"), 200)

class Seller(Resource):

    def post(self):
        data = request.get_json()

        pin = data['pin']
        level = data['level']

        for i in range(0, len(pin)):
            user_input = {"pin": pin[i], "level": level}
            buyercol.insert_one(user_input)
        return make_response(jsonify("Inserted Data!"), 200)

# adding the defined resources along with their corresponding urls
api.add_resource(SellerRange, '/api/seller')
api.add_resource(Buyer, '/api/sellerdata')
api.add_resource(Seller, '/api/buyerdata')


# driver function
if __name__ == '__main__':

    app.run(debug=True)
