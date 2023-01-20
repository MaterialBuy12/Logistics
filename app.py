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

    # def post(self):
    #     data = request.get_json()

    #     title = "Deep"

    #     rating1 = data['rating1']
    #     rating2 = data['rating2']
    #     rating3 = data['rating3']
    #     rating4 = data['rating4']
    #     rating5 = data['rating5']
    #     rating6 = data['rating6']
    #     rating7 = data['rating7']
    #     rating8 = data['rating8']
    #     rating9 = data['rating9']
    #     rating10 = data['rating10']
    #     rating11 = data['rating11']
    #     rating12 = data['rating12']
    #     rating13 = data['rating13']
    #     rating14 = data['rating14']
    #     rating15 = data['rating15']

    #     ran1 = data['ran1']
    #     ran2 = data['ran2']
    #     ran3 = data['ran3']
    #     ran4 = data['ran4']
    #     ran5 = data['ran5']
    #     ran6 = data['ran6']
    #     ran7 = data['ran7']
    #     ran8 = data['ran8']
    #     ran9 = data['ran9']
    #     ran10 = data['ran10']
    #     ran11 = data['ran11']
    #     ran12 = data['ran12']
    #     ran13 = data['ran13']
    #     ran14 = data['ran14']
    #     ran15 = data['ran15']
    #     # rating = data['rating']
    #     # ran = data['range']

    #     user_input = {"title": title,
    #                   "rating1": rating1,
    #                   "rating2": rating2,
    #                   "rating3": rating3,
    #                   "rating4": rating4,
    #                   "rating5": rating5,
    #                   "rating6": rating6,
    #                   "rating7": rating7,
    #                   "rating8": rating8,
    #                   "rating9": rating9,
    #                   "rating10": rating10,
    #                   "rating11": rating11,
    #                   "rating12": rating12,
    #                   "rating13": rating13,
    #                   "rating14": rating14,
    #                   "rating15": rating15,
    #                   "ran1": ran1,
    #                   "ran2": ran2,
    #                   "ran3": ran3,
    #                   "ran4": ran4,
    #                   "ran5": ran5,
    #                   "ran6": ran6,
    #                   "ran7": ran7,
    #                   "ran8": ran8,
    #                   "ran9": ran9,
    #                   "ran10": ran10,
    #                   "ran11": ran11,
    #                   "ran12": ran12,
    #                   "ran13": ran13,
    #                   "ran14": ran14,
    #                   "ran15": ran15,
    #                   }

    #     mycol.insert_one(user_input)

    #     return make_response(jsonify("Data inserted!"), 200)

    @cross_origin(origins="*")
    def put(self):
        data = request.get_json()
        rating = data['rating']
        ran = data['range']

        user_input = {"rating":rating, "ran": ran}

        return make_response(jsonify("Data Updated"), 200)

    def put(self):
        data = request.get_json()

        # query={"_id":{"$eq":"63a95d60373e4f783563f66d"}}
        # presentdata =  mycol.find(query)
        # new_data = {'$set': data}
        # mycol.find_one_and_update({"title": "krupesh"}, {'$set': data})

        mycol.update_one({"title": "krupesh"}, {'$set': data})
        return make_response(jsonify("Data Updated"), 200)

    def get(self):
        data = [doc for doc in mycol.find()]

        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)


class Buyer(Resource):

    def post(self):
        data = request.get_json()

        pin = data['pin']
        level = data['level']

        li = list(pin.split(","))

        for i in range(0, len(li)):
            user_input = {"pin": li[i], "level": level}
            buyercol.insert_one(user_input)
        return make_response(jsonify("Inserted Data!"), 200)


class Seller(Resource):

    def post(self):
        data = request.get_json()

        pin = data['pin']
        level = data['level']

        li = list(pin.split(","))

        for i in range(0, len(li)):
            user_input = {"pin": li[i], "level": level}
            sellercol.insert_one(user_input)
        return make_response(jsonify("Inserted Data!"), 200)


class Transport(Resource):

    def post(self):

        data = request.get_json()

        name = data['name']
        mobileno = data['mobileno']
        emailid = data['emailid']
        gst = data['gst']
        address = data['address']
        rate = data['rate']

        user_input = {"name": name, "mobileno": mobileno,
                      "emailid": emailid, "gst": gst, "address": address, "rate": rate}
        transportcol.insert_one(user_input)

        return make_response(jsonify("Inserted Data!"), 200)

# adding the defined resources along with their corresponding urls
api.add_resource(SellerRange, '/api/seller')
api.add_resource(Buyer, '/api/sellerdata')
api.add_resource(Seller, '/api/buyerdata')


# driver function
if __name__ == '_main_':

    app.run(debug=True)
