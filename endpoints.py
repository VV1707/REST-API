from flask_pymongo import pymongo
from flask import jsonify, request


con_string = "mongodb+srv://vidya:vidyavarshini@cluster0.hkoolhy.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('demodb')

user_collection = pymongo.collection.Collection(db, 'democoll')
print("MongoDB connected Successfully")


def project_api_routes(endpoints):
    @endpoints.route('/begin', methods=['GET'])
    def begin():
        res = 'HELLO'
        print("HELLO")
        return res

    @endpoints.route('/create', methods=['POST'])
    def add_user():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    @endpoints.route('/read',methods=['GET'])
    def display_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
            }
            output = [{'STUDENT ID' : user['id'], 'STUDENT NAME' : user['name']} for user in users]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/update',methods=['PUT'])
    def update_user():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"STUDENT ID":req_body['id']}, {"$set": req_body['updated_user_body']})
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/delete',methods=['DELETE'])
    def delete_user():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"STUDENT ID":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


    return endpoints
