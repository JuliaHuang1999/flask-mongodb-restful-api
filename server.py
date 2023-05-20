import app
from flask import Flask, jsonify, request
from flask_pymongo import pymongo, PyMongo
import json
from bson import json_util, ObjectId
from bson.json_util import dumps

# Connect with MongoDB Atlas
DB_URI = "<connection_string>"
client = pymongo.MongoClient(DB_URI)
db = client.get_database('flask_mongodb_atlas')

app = Flask(__name__)
app.config["MONGO_URI"] = DB_URI
mongo = PyMongo(app)


# POST
# curl -X POST http://127.0.0.1:9000/add/Sofia/2023-01-04/Transportation/Gas/40
@app.route('/add/<name>/<date>/<cat>/<item>/<int:price>', methods=['POST'])
def post_doc(name, date, cat, item, price):

    doc = db.collection.insert_one(
        {"name": name, "date": date, "category": cat, "item": item, "price": price})
    new_id = json.loads(json_util.dumps(doc.inserted_id))

    resp = {"database": request.url_root,
            "path": request.path,
            "full path": request.full_path,
            }
    print(resp)

    resp2 = jsonify('Doc added successfully!')
    print(resp2)

    return "Document added successfully! Auto generated _id: " + str(list(new_id.values())[0])


# PUT
# curl -X PUT http://127.0.0.1:9000/add/16888/Anna/2023-01-04/Transportation/Gas/40
@app.route('/add/<id>/<name>/<date>/<cat>/<item>/<int:price>', methods=['PUT'])
def put_doc(id, name, date, cat, item, price):

    doc = db.collection.insert_one(
        {"_id": id, "name": name, "date": date, "category": cat, "item": item, "price": price})

    resp = {"database": request.url_root,
            "path": request.path,
            "full path": request.full_path,
            }
    print(resp)

    resp2 = jsonify('Document added successfully!')
    print(resp2)

    return "Document added successfully!"


# GET ONE Document: by id
# curl -X GET http://127.0.0.1:9000/id/642b64638f7406e65b12eed1
@app.route('/id/<id>', defaults={'myPath': ''})
@app.route('/<path:myPath>', methods=['GET'])
def get_one_doc_id(id, myPath):

    try:
        doc = db.collection.find_one({"_id": ObjectId(id)})
        doc_json = json.loads(json_util.dumps(doc))
    except:
        return not_found()

    resp = {"database": request.url_root,
            "path": request.path,
            "full path": request.full_path,
            "myPath": myPath
            }
    print(resp)

    return doc_json


# GET Document w/ filter
@app.route('/filter', methods=['GET'])
def filter_doc():

    param = request.args.to_dict()
    filterkeys = ["orderby", "limit", "skip", "asc", "startAt", "endAt"]
    filter = sorted(set(filterkeys).intersection(set(list(param.keys()))))
    sort_key = dict((d, param.pop(d)) for d in filter)

    # orderby
    if 'orderby' in sort_key:
        sor = sort_key['orderby']
    else:
        sor = "$natural"

    # startAt
    if "startAt" in sort_key:
        lowerbound = int(sort_key['startAt'])
    else:
        lowerbound = 0

    # endAt
    if "endAt" in sort_key:
        upperbound = int(sort_key['endAt'])
    else:
        upperbound = 1000000000

    if "startAt" in sort_key or "endAt" in sort_key:
        param = {sor: {"$gt": lowerbound, "$lt": upperbound}}

    # asc
    if 'asc' in sort_key:
        asc = int(sort_key['asc'])
    else:
        asc = 1

    # skip
    if 'skip' in sort_key:
        ski = int(sort_key['skip'])
    else:
        ski = 0

    # limit
    if 'limit' in sort_key:
        lim = int(sort_key['limit'])
    else:
        lim = 0

    cursor = db.collection.find(param).sort(sor, asc).skip(ski).limit(lim)
    cursor_lst = list(cursor)
    all_docs = json.loads(json_util.dumps(cursor_lst))
    return all_docs


# PATCH
# curl -X PATCH http://127.0.0.1:9000/update/642cf25b714bb5917baa372e/Alice/2022-09-30/Transportation/Uber/20
@app.route('/update/<id>/<name>/<date>/<cat>/<item>/<int:price>', methods=['PATCH'])
def update_doc(id, name, date, cat, item, price
               ):

    db.collection.update_one({'_id': ObjectId(id)}, {'$set': {
                             "name": name, "date": date, "category": cat, "item": item, "price": price}})
    return 'Document updated successfully!'


# DELETE
# curl -X DELETE http://127.0.0.1:9000/642b662a9e7bab58ac120cc6
@app.route('/<id>', methods=['DELETE'])
def delete_doc(id):
    db.collection.delete_one({'_id': ObjectId(id)})
    return 'Document deleted successfully!'


# Erorr Handler
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    app.run(debug=True, port=9000)