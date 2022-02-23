import pymongo
from pymongo import MongoClient
import os


"""took submit and display function out of flask_brevets for testing purposes,
also changed submit to take a dictionary, which a request object is, so we can
test more easily. """
def submit(dict):
    if(not dict):
        #request contains no data
        return 204
    if(dict['checkpoints'] == []):
        #request contains checkpoints to store
        return 204
    else:

        data = {
        'dist': dict['dist'],
        'start': dict['start'],
        'checkpoints': dict['checkpoints']
        }
        client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
        brevetDB = client.brevetDB
        itemId = brevetDB.posts.insert_one(data)
        client.close()
        return 200


def display():
    client = MongoClient('mongodb://mymongodb', 27017)
    if(not client):
        #cant connect to the client
        return 500,500,500

    brevetDB = client.brevetDB
    data = brevetDB.posts.find_one(sort=[('_id', pymongo.DESCENDING)])
    if(not data):
        #we do not have any data
        return 204,204,204

    dist = data["dist"]
    start = data["start"]
    checkpoints = data["checkpoints"]

    client.close()
    return dist,start,checkpoints
