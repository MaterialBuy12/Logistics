# using flask_restful
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import pymongo
import json
from bson import json_util
from flask_cors import CORS, cross_origin
import pandas as pd
# import os
# import urllib.request
# from werkzeug.utils import secure_filename

# creating the flask app
# UPLOAD_FOLDER = '/uploads'
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app, supports_credentials=True)
# creating an API object
api = Api(app)

client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['materialbuy']
mycol = mydb['sellerrange']
sellercol = mydb['sellercol']
buyercol = mydb['buyercol']
transportcol = mydb['transport']
weightcol = mydb['weightcol']
csvcol = mydb['csvcol']

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

        # query={"_id":{"$eq":"63a95d60373e4f783563f66d"}}
        # presentdata =  mycol.find(query)
        # new_data = {'$set': data}
        mycol.update_one({"title": "Deep"}, {'$set': data})

        return make_response(jsonify("Data Updated"), 200)

    def get(self):
        data = [doc for doc in mycol.find()]

        if (len(data) == 0):
            print("Run")
            user_input = {"title": "Deep",
                          "rating1": "0",
                          "rating2": "0",
                          "rating3": "0",
                          "rating4": "0",
                          "rating5": "0",
                          "rating6": "0",
                          "rating7": "0",
                          "rating8": "0",
                          "rating9": "0",
                          "rating10": "0",
                          "rating11": "0",
                          "rating12": "0",
                          "rating13": "0",
                          "rating14": "0",
                          "rating15": "0",
                          "ran1": "0",
                          "ran2": "0",
                          "ran3": "0",
                          "ran4": "0",
                          "ran5": "0",
                          "ran6": "0",
                          "ran7": "0",
                          "ran8": "0",
                          "ran9": "0",
                          "ran10": "0",
                          "ran11": "0",
                          "ran12": "0",
                          "ran13": "0",
                          "ran14": "0",
                          "ran15": "0",
                          }

            mycol.insert_one(user_input)

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

    def get(self):

        data = [doc for doc in transportcol.find()]

        data = data[::-1]

        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)

    def delete(self):

        data = request.get_json()

        transportcol.delete_one({"name": data['name']})

        return make_response(jsonify("Data Deleted!"), 200)


class WeightRange(Resource):

    def post(self):

        data = request.get_json()

        ran1 = data['ran1']
        ran2 = data['ran2']
        ran3 = data['ran3']
        ran4 = data['ran4']
        ran5 = data['ran5']
        ran6 = data['ran6']
        ran7 = data['ran7']
        ran8 = data['ran8']
        ran9 = data['ran9']
        ran10 = data['ran10']

        weighting1 = data['weighting1']
        weighting2 = data['weighting2']
        weighting3 = data['weighting3']
        weighting4 = data['weighting4']
        weighting5 = data['weighting5']
        weighting6 = data['weighting6']
        weighting7 = data['weighting7']
        weighting8 = data['weighting8']
        weighting9 = data['weighting9']
        weighting10 = data['weighting10']

        user_input = {
            "ran1": ran1,
            "ran2": ran2,
            "ran3": ran3,
            "ran4": ran4,
            "ran5": ran5,
            "ran6": ran6,
            "ran7": ran7,
            "ran8": ran8,
            "ran9": ran9,
            "ran10": ran10,
            "weighting1": weighting1,
            "weighting2": weighting2,
            "weighting3": weighting3,
            "weighting4": weighting4,
            "weighting5": weighting5,
            "weighting6": weighting6,
            "weighting7": weighting7,
            "weighting8": weighting8,
            "weighting9": weighting9,
            "weighting10": weighting10,
        }

        weightcol.insert_one(user_input)

        return make_response(jsonify("Data Inserted!"), 200)

    def put(self):
        data = request.get_json()

        weightcol.find_one_and_update({{"title": "Deep"}}, {'$set': data})

        return make_response(jsonify("Data Updated"), 200)

    def get(self):
        data = [doc for doc in weightcol.find()]

        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)


class RateChart(Resource):

    def post(self):

        data = request.get_json()
        url = data['url']
        
        # df = pd.read_csv("credits.csv")
        # data = df.to_dict("records")

        # csvcol.insert_many(data, ordered=True)

        # file = request.files['file']

        # if file:
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     resp = jsonify({'message' : 'File successfully uploaded'})
        #     resp.status_code = 201
        #     return resp

        return make_response(jsonify("Uploaded Csv"), 200)



# adding the defined resources along with their corresponding urls
api.add_resource(SellerRange, '/api/seller')
api.add_resource(Buyer, '/api/sellerdata')
api.add_resource(Seller, '/api/buyerdata')
api.add_resource(Transport, '/api/transport')
api.add_resource(WeightRange, '/api/weight')
api.add_resource(RateChart, '/api/ratechart')


# driver function
if __name__ == '__main__':

    app.run(debug=True)
