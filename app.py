# using flask_restful
import io
from flask import Flask, Response, jsonify, request, make_response
from flask_restful import Resource, Api
import pymongo
import json
from bson import json_util, ObjectId
import csv
from flask_cors import CORS, cross_origin
#import pgeocode
import requests
import http.client

# creating the flask app

app = Flask(__name__)
# TEMPLATES_AUTO_RELOAD = True
# CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, support_credentials=True)
# creating an API object

api = Api(app)

client = pymongo.MongoClient(
    'mongodb+srv://db_admin:admin123@materialbuy-dev.ywwohb6.mongodb.net/?retryWrites=true&w=majority')
mydb = client['materialbuy']
mycol = mydb['sellerrange']
sellercol = mydb['sellercol']
buyercol = mydb['buyercol']
transportcol = mydb['transport']
weightcol = mydb['weightcol']
csvcol = mydb['csvcol']

#ANKIT LOGISTICS
#CODE STARTS HERE

sellers = []
codeB = []
buyersellerdist = []
codeC= []
logicode = []
shipCosts = []

newdb = client['test']
products = newdb['products']
productrequests = newdb['productrequests']
warehouses = newdb['warehouses']
wtflag = ""

def find_prices_by_productid(productid):
    query = {"productid": productid}
    result = productrequests.find(query)
    prices_list = [doc.get("price") for doc in result]
    return prices_list

def get_distance(api_key, origin_pincode, destination_pincode):
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    origin = f'{origin_pincode}, India'  # You can replace 'India' with the relevant country
    destination = f'{destination_pincode}, India'
    
    params = {
        'origins': origin,
        'destinations': destination,
        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    try:
        distance_text = data['rows'][0]['elements'][0]['distance']['text']
        distance_text = ''.join(char for char in distance_text if char.isdigit())
        distance_value = data['rows'][0]['elements'][0]['distance']['value']
        return distance_text, distance_value
    except KeyError:
        print("Error: Unable to retrieve distance information.")
        return None, None
    
def shipcostcalc(pincode, productid, variantid, quantity):
    curr_buyerpc = pincode
    curr_pid = productid
    curr_vid = variantid
    curr_qty = quantity

    codeA = buyerpin(curr_buyerpc)
    print(codeA, "CODEA")
    variant_details = fetch_variant_details(curr_pid, curr_vid)
    
    if variant_details:
        print(f"Variant details for product {curr_pid}, variant {curr_vid}:")
        # print(variant_details)
        deadwt = variant_details.get('weight7A', 'N/A')
        deadwtunit = variant_details.get('weightunit7A', 'N/A')
        
        if deadwtunit == "g":
            deadwt = float(deadwt) / 1000
        deadwt = float(deadwt) * curr_qty
        volwt = variant_details.get('volumetricweight7B', 'N/A')
        volwtunit = variant_details.get('volumetricunit7B', 'N/A')
        
        if volwtunit == "g":
            volwt = float(volwt) / 1000
        
        box1 = variant_details.get('unit18A', '')
        box2 = variant_details.get('unit18B', 'N/A')
        box3 = variant_details.get('unit18C', 'N/A')
        box4 = variant_details.get('unit18D', 'N/A')
        volbox1 = variant_details.get('vol18E', 'N/A')
        volbox2 = variant_details.get('vol18F', 'N/A')
        volbox3 = variant_details.get('vol18G', 'N/A')
        volbox4 = variant_details.get('vol18H', 'N/A')
        print(deadwt, volwt, box1, box2, box3, box4, volbox1, volbox2, volbox3, volbox4)

        if box1 == '':
            actwt = deadwt
            result_boxes = 0
            total_weight = actwt
        else:
            result_boxes, total_weight = pack_boxes(int(curr_qty), int(box1), int(box2), int(box3), int(box4),
                                                float(volbox1), float(volbox2), float(volbox3), float(volbox4))
            print("Number of boxes used for each type:")
            print(result_boxes)
            print("Total weight of boxes used:", total_weight)
            volwt = total_weight
            total_weight = "VOL: "+str(total_weight)+" DEAD: "+str(deadwt)
            actwt = max(deadwt, volwt)

        shipType = ""
        
        if actwt <= 10:
            print("3PL")
            shipType = "3PL"
            vendorwarehouse = fetch_vendor_warehouse_ids(curr_vid)
            print(vendorwarehouse)
            prices_result = find_prices_by_productid(curr_vid)
            print("new")
            print(prices_result)
            sellers = []
            
            for request in vendorwarehouse:
                print(f"Vendor ID: {request.get('vendorid')}, Warehouse ID: {request.get('warehouseid')}")
                given_warehouseid = request.get('warehouseid')
                print(given_warehouseid)
                pincode_result = fetch_pincode_by_warehouseid(given_warehouseid)
                
                if pincode_result:
                    print(f"Pincode(s) for Warehouse ID '{given_warehouseid}':")
                    result_string = pincode_result[0]
                    print(result_string)
                else:
                    print(f"No matching documents found for Warehouse ID '{given_warehouseid}'.")
                
                sellers.append(result_string)
            
            print(sellers)
            conn = http.client.HTTPSConnection("apiv2.shiprocket.in")
            payload = json.dumps({
            "email": "materialbuy.management@gmail.com",
            "password": "Material@3007"
            })
            headers = {
            'Content-Type': 'application/json'
            }
            try:
                conn.request("POST", "/v1/external/auth/login", payload, headers)
                res = conn.getresponse()

                if res.status == 200:
                    data = res.read().decode("utf-8")
                    # Extract the token from the response
                    token = json.loads(data).get('token')
                    #print("Token:", token)
                else:
                    print(f"Error: {res.status} - {res.reason}")

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                conn.close()
            pl3cost = []
            token = 'Bearer '+ token
            print(curr_buyerpc)
            for seller_curr in sellers:
                conn = http.client.HTTPSConnection("apiv2.shiprocket.in")
                payload = json.dumps({
                "pickup_postcode": seller_curr,
                "delivery_postcode": curr_buyerpc,
                "cod": "0",
                "weight": actwt
                })
                headers = {
                'Content-Type': 'application/json',
                'Authorization': token
                }
                conn.request("GET", "/v1/external/courier/serviceability/", payload, headers)
                res = conn.getresponse()
                dataa = res.read()
                #print(dataa.decode("utf-8"))
                json_data_str = dataa.decode('utf-8')
                data = json.loads(json_data_str)

                # Extracting the available courier companies
                courier_companies = data.get("data", {}).get("available_courier_companies", [])
                conn.close()


                # Check if there are any courier companies
                if courier_companies:
                    # Find the courier company with the minimum freight charge
                    min_freight_company = min(courier_companies, key=lambda x: x.get("freight_charge", float('inf')))

                    # Extract relevant information
                    min_freight_courier_name = min_freight_company.get("courier_name")
                    min_freight_charge = min_freight_company.get("freight_charge")

                    # Display the result
                    print(f"The courier company with the minimum freight charge is '{min_freight_courier_name}' with a charge of {min_freight_charge} INR.")
                    pl3cost.append(min_freight_charge)   
                    print(pl3cost)         
                else:
                    print("No courier companies available.")
                shipCosts = []
                shipCosts = pl3cost
                total_weight = actwt
                print(shipCosts)
                print(vendorwarehouse)
                print(total_weight)
                print(result_boxes)
                print(shipType)
            return shipCosts, vendorwarehouse, total_weight, result_boxes, shipType, prices_result
        else:
            print("TRANSPORT")
            shipType = "TRANSPORT"

            all_values = fetch_all_documents()
            
            for document in all_values:
                print("document")
            
            wt1 = float(document.get('weighting1', 'N/A'))
            wt2 = float(document.get('weighting2', 'N/A'))
            wt3 = float(document.get('weighting3', 'N/A'))
            wt4 = float(document.get('weighting4', 'N/A'))
            wt5 = float(document.get('weighting5', 'N/A'))
            wt6 = float(document.get('weighting6', 'N/A'))
            wt7 = float(document.get('weighting7', 'N/A'))
            wt8 = float(document.get('weighting8', 'N/A'))
            wt9 = float(document.get('weighting9', 'N/A'))
            wt10 = float(document.get('weighting10', 'N/A'))
            
            if actwt <= wt1:
                codeD = '0'
            elif wt1 < actwt <= wt2:
                codeD = '1'
            elif wt2 < actwt <= wt3:
                codeD = '2'
            elif wt3 < actwt <= wt4:
                codeD = '3'
            elif wt4 < actwt <= wt5:
                codeD = '4'
            elif wt5 < actwt <= wt6:
                codeD = '5'
            elif wt6 < actwt <= wt7:
                codeD = '6'
            elif wt7 < actwt <= wt8:
                codeD = '7'
            elif wt8 < actwt <= wt9:
                codeD = '8'
            elif wt9 < actwt <= wt10:
                codeD = '9'
            
            print(codeD, "CODED")
            vendorwarehouse = fetch_vendor_warehouse_ids(curr_vid)
            print(vendorwarehouse)
            prices_result = find_prices_by_productid(curr_vid)
            print("new")
            print(prices_result)
            sellers = []
            
            for request in vendorwarehouse:
                print(f"Vendor ID: {request.get('vendorid')}, Warehouse ID: {request.get('warehouseid')}")
                given_warehouseid = request.get('warehouseid')
                print(given_warehouseid)
                pincode_result = fetch_pincode_by_warehouseid(given_warehouseid)
                
                if pincode_result:
                    print(f"Pincode(s) for Warehouse ID '{given_warehouseid}':")
                    result_string = pincode_result[0]
                    print(result_string)
                else:
                    print(f"No matching documents found for Warehouse ID '{given_warehouseid}'.")
                
                sellers.append(result_string)
            
            print(sellers)
            codeB = [str(sellerpin(seller)) for seller in sellers]
            print(codeB, "CODEB")
            buyersellerdist = []
            #dist = pgeocode.GeoDistance('in')
            
            for seller_pincode in sellers:
                #distance = dist.query_postal_code(curr_buyerpc, seller_pincode)
                api_key = 'AIzaSyCfu3BHDymFSIcPsub6tlOqpjdbxT3O09Q'
                distance_text, distance_value = get_distance(api_key, curr_buyerpc, seller_pincode)
                buyersellerdist.append(float(distance_text))
            
            print(buyersellerdist)
            all_values = fetch_all_documentss()
            
            for document in all_values:
                print("document")
            
            dist1 = float(document.get('rating1', 'N/A'))
            dist2 = float(document.get('rating2', 'N/A'))
            dist3 = float(document.get('rating3', 'N/A'))
            dist4 = float(document.get('rating4', 'N/A'))
            dist5 = float(document.get('rating5', 'N/A'))
            dist6 = float(document.get('rating6', 'N/A'))
            dist7 = float(document.get('rating7', 'N/A'))
            dist8 = float(document.get('rating8', 'N/A'))
            dist9 = float(document.get('rating9', 'N/A'))
            dist10 = float(document.get('rating10', 'N/A'))
            dist11 = float(document.get('rating11', 'N/A'))
            dist12 = float(document.get('rating12', 'N/A'))
            dist13 = float(document.get('rating13', 'N/A'))
            dist14 = float(document.get('rating14', 'N/A'))
            dist15 = float(document.get('rating15', 'N/A'))
            codeC = []
            
            for distanceval in buyersellerdist:
                if distanceval <= dist1:
                    distanceval = 'A'
                elif dist1 < distanceval <= dist2:
                    distanceval = 'B'
                elif dist2 < distanceval <= dist3:
                    distanceval = 'C'
                elif dist3 < distanceval <= dist4:
                    distanceval = 'D'
                elif dist4 < distanceval <= dist5:
                    distanceval = 'E'
                elif dist5 < distanceval <= dist6:
                    distanceval = 'F'
                elif dist6 < distanceval <= dist7:
                    distanceval = 'G'
                elif dist7 < distanceval <= dist8:
                    distanceval = 'H'
                elif dist8 < distanceval <= dist9:
                    distanceval = 'I'
                elif dist9 < distanceval <= dist10:
                    distanceval = 'J'
                elif dist10 < distanceval <= dist11:
                    distanceval = 'K'
                elif dist11 < distanceval <= dist12:
                    distanceval = 'L'
                elif dist12 < distanceval <= dist13:
                    distanceval = 'M'
                elif dist13 < distanceval <= dist14:
                    distanceval = 'N'
                elif dist14 < distanceval <= dist15:
                    distanceval = 'O'
                
                codeC.append(distanceval)
            
            print(codeC, "CODEC")
            
            # Ensure that buyersellerdist and codeB have the same length
            min_length = min(len(buyersellerdist), len(codeB))
            buyersellerdist = buyersellerdist[:min_length]
            codeB = codeB[:min_length]
            
            # Update logicode using zip to iterate over both lists simultaneously
            logicode = [codeA + codeB_val + codeD + codeC[i] for i, codeB_val in enumerate(codeB)]
            
            print("CODES: ", logicode)
            
            shipCosts = []
            
            for code in logicode:
                corresponding_value = find_value_by_key(code)
                
                if corresponding_value is not None:
                    print(f"Corresponding value for key '{code}': {corresponding_value}")
                    print(corresponding_value,actwt)
                    shipCosts.append(float(corresponding_value) * actwt)
                else:
                    print(f"No matching document found for key '{code}'.")
            
            return shipCosts, vendorwarehouse, total_weight, result_boxes, shipType, prices_result
    else:
        print(f"No data found for product {curr_pid}, variant {curr_vid}")

# You can call this function with your input values
# shipcostcalc(your_pincode, your_productid, your_variantid, your_quantity)


def find_value_by_key(key_to_match):
    query = {"values": {"$elemMatch": {"$elemMatch": {"$eq": key_to_match}}}}
    result = csvcol.find_one(query)

    if result:
        values_array = result.get("values", [])

        for sub_array in values_array:
            if key_to_match in sub_array:
                index = sub_array.index(key_to_match)
                if index + 1 < len(sub_array):
                    return sub_array[index + 1]
    
    return None



def pack_boxes(total_quantity, x1, x2, x3, x4, w1, w2, w3, w4):
    remaining_quantity = total_quantity
    boxes_used = {1: 0, 2: 0, 3: 0, 4: 0}
    total_weight = 0

    while remaining_quantity > 0:
        if remaining_quantity >= x4:
            boxes_used[4] += remaining_quantity // x4
            total_weight += (remaining_quantity // x4) * w4
            remaining_quantity %= x4
        elif remaining_quantity >= x3:
            boxes_used[3] += remaining_quantity // x3
            total_weight += (remaining_quantity // x3) * w3
            remaining_quantity %= x3
        elif remaining_quantity >= x2:
            boxes_used[2] += remaining_quantity // x2
            total_weight += (remaining_quantity // x2) * w2
            remaining_quantity %= x2
        elif remaining_quantity >= x1:
            boxes_used[1] += remaining_quantity // x1
            total_weight += (remaining_quantity // x1) * w1
            remaining_quantity %= x1
        elif 0 < remaining_quantity < x1:
            boxes_used[1] += 1
            total_weight += 1*w1
            remaining_quantity = 0
            break

    return boxes_used, total_weight

def fetch_variant_details(product_id, variant_id):
    query = {"_id": product_id}
    product = products.find_one(query)
    if product:
        variations_array = product.get("variations", [])
        #print(variations_array)
        for variation in variations_array:
            if variation.get("_id") == variant_id:
                return variation
        else:
            return None  # Variant with the specified ID not found
    else:
        return None  # Product with the specified ID not found

def buyerpin(query_pin):
    query = {"pin": query_pin}
    result = buyercol.find_one(query)
    if result:
        return result.get('level', None)
    else:
        return None
    
def sellerpin(query_pin):
    query = {"pin": query_pin}
    result = sellercol.find_one(query)
    if result:
        return result.get('level', None)
    else:
        return None
    
def fetch_all_documents():
    cursor = weightcol.find()
    all_documents = list(cursor)
    return all_documents

def fetch_all_documentss():
    cursor = mycol.find()
    all_documents = list(cursor)
    return all_documents

def fetch_vendor_warehouse_ids(product_id):
    query = {"productid": product_id}
    projection = {"vendorid": 1, "warehouseid": 1, "_id": 0}  # Include only vendorid and warehouseid in the result
    result = productrequests.find(query, projection)
    product_requests = list(result)
    return product_requests

def fetch_pincode_by_warehouseid(given_warehouseid):
    query = {"_id": given_warehouseid}
    result = warehouses.find(query)
    pincode_list = [doc.get("pincode") for doc in result]
    return pincode_list

#high = shipcostcalc('401202',ObjectId("65b76d83c1dc780034f6ac11"),ObjectId("65b76deac1dc780034f6ac13"),2)

#CODE ENDS HERE
#ANKIT LOGISTICS
        
app.route('/', methods=['GET'])


def home():
    return "Flask app running"


class Home(Resource):
    def get(self):
        return make_response(jsonify("Flask App running"), 200)


class SellerRange(Resource):

    def post(self):
        data = request.get_json()

        title = data['title']

        rating1 = data['rating1']
        rating2 = data['rating2']
        rating3 = data['rating3']
        rating4 = data['rating4']
        rating5 = data['rating5']
        rating6 = data['rating6']
        rating7 = data['rating7']
        rating8 = data['rating8']
        rating9 = data['rating9']
        rating10 = data['rating10']
        rating11 = data['rating11']
        rating12 = data['rating12']
        rating13 = data['rating13']
        rating14 = data['rating14']
        rating15 = data['rating15']

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
        ran11 = data['ran11']
        ran12 = data['ran12']
        ran13 = data['ran13']
        ran14 = data['ran14']
        ran15 = data['ran15']
        # rating = data['rating']
        # ran = data['range']

        user_input = {"title": title,
                      "rating1": rating1,
                      "rating2": rating2,
                      "rating3": rating3,
                      "rating4": rating4,
                      "rating5": rating5,
                      "rating6": rating6,
                      "rating7": rating7,
                      "rating8": rating8,
                      "rating9": rating9,
                      "rating10": rating10,
                      "rating11": rating11,
                      "rating12": rating12,
                      "rating13": rating13,
                      "rating14": rating14,
                      "rating15": rating15,
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
                      "ran11": ran11,
                      "ran12": ran12,
                      "ran13": ran13,
                      "ran14": ran14,
                      "ran15": ran15,
                      }

        mycol.insert_one(user_input)

        return make_response(jsonify("Data inserted!"), 200)

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
        print("data", data)
        if (len(data) == 0):
            print("h")

            user_input = {"title": "krupesh",
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

    def get(self):
        query = request.args.get('pin')
        objid = request.args.get('id')
        # print(query)
        if query:
            data = {"data": buyercol.find({"pin": query})}
        elif objid:
            data = buyercol.find_one({"_id": ObjectId(objid)})
        else:
            data = [doc for doc in buyercol.find().sort(
            '_id', pymongo.DESCENDING)]
        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)

    def put(self):
        data = request.get_json()
        updatebody = {
            "$set": {
                "pin": data['pin'],
                "level": data['level']
            }
        }
        buyercol.update_one({"_id": ObjectId(data['id'])}, update=updatebody)
        return make_response(jsonify("Data updated"), 200)

    def delete(self):
        data = request.get_json()
        buyercol.delete_one({"_id": ObjectId(data['id'])})
        return make_response(jsonify("Data deleted"), 200)


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

    def get(self):
        query = request.args.get('pin')
        objid = request.args.get('id')
        # print(query)
        if query:
            data = {"data": sellercol.find({"pin": query})}
        elif objid:
            data = sellercol.find_one({"_id": ObjectId(objid)})
        else:
            data = [doc for doc in sellercol.find().sort(
            '_id', pymongo.DESCENDING)]
        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)
    
    def put(self):
        data = request.get_json()
        updatebody = {
            "$set": {
                "pin": data['pin'],
                "level": data['level']
            }
        }
        sellercol.update_one({"_id": ObjectId(data['id'])}, update=updatebody)
        return make_response(jsonify("Data updated"), 200)

    def delete(self):
        data = request.get_json()
        sellercol.delete_one({"_id": ObjectId(data['id'])})
        return make_response(jsonify("Data deleted"), 200)

class Shipping(Resource):
    def post(self):
        data = request.get_json()
        pincode = data['pincode']
        productid = data['productid']
        variantid = data['variantid']
        quantity = data['quantity']

        shipCost, vendorWareHouse, totalBoxesWeight, boxDetails, shipType =  shipcostcalc(pincode, ObjectId(productid), ObjectId(variantid), quantity)

        vendorWareHouse = [
        {
            'vendorid': str(request.get('vendorid')),  # Convert ObjectId to string
            'warehouseid': str(request.get('warehouseid'))  # Convert ObjectId to string
        }
        for request in vendorWareHouse
    ]
        
        output = {
            "shipCost": shipCost,
            "vendorWareHouse": vendorWareHouse,
            "total_weight": totalBoxesWeight,
            "boxDetails": boxDetails,
            "shipType": shipType
        }
        
        return make_response(jsonify(output), 200)
                                
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
        query = request.args.get('name')
        if query:
            data = [doc for doc in transportcol.find({"name": {
                "$regex": query
            }})]
        else:
            data = [doc for doc in transportcol.find()]
        data = data[::-1]

        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)

    def delete(self):
        print("wre", request.get_json())
        data = request.get_json()
        print("trandelete")

        transportcol.delete_one({"name": data['name']})

        return make_response(jsonify("Data Deleted!"), 200)


class WeightRange(Resource):

    def post(self):

        d = [doc for doc in weightcol.find()]

        if len(d) > 0:
            weightcol.delete_one({"title": "krupesh"})

        data = request.get_json()

        title = data['title']

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
            "title": title,
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

    def get(self):
        data = [doc for doc in weightcol.find()]

        return make_response(jsonify(json.loads(json_util.dumps(data))), 200)


class RateChart(Resource):

    def post(self):

        data = request.get_json()
        data1 = [doc for doc in csvcol.find()]
        if (len(data1) > 0):
            csvcol.drop()
            csvcol.insert_one({"values": data})
        else:
            csvcol.insert_one({"values": data})

        print("url", data)
        return make_response(jsonify("Uploaded Csv"), 200)

    def get(self):
        data = [doc for doc in csvcol.find()]
        print(data[0]['values'])
        values = data[0]['values']

        if values:
            output = io.StringIO()
            writer = csv.writer(output)
            for row in values:
                writer.writerow(row)

                # Prepare the CSV response
            response = Response(output.getvalue(), content_type='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
            return response
        return make_response(jsonify("No data found"), 404)

        # csvcol.insert_one( )
        # df = pd.read_csv("credits.csv")
        # data = df.to_dict("records")

        # file = request.files['file']

        # if file:
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     resp = jsonify({'message' : 'File successfully uploaded'})
        #     resp.status_code = 201
        #     return resp     

# adding the defined resources along with their corresponding urls
api.add_resource(Home, '/')
api.add_resource(SellerRange, '/api/seller')
api.add_resource(Buyer, '/api/buyerdata')
api.add_resource(Seller, '/api/sellerdata')
api.add_resource(Transport, '/api/transport')
api.add_resource(WeightRange, '/api/weight')  # ..
api.add_resource(RateChart, '/api/ratechart')
api.add_resource(Shipping, '/api/shipping')

# driver function
if __name__ == '_main_':

    app.run(debug=True)