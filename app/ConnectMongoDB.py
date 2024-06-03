import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

dotenv_path = os.path.join(os.path.dirname(__file__), '../config/.env')
load_dotenv(dotenv_path)

Mongo_client = MongoClient(os.getenv("ULI"), tls=True, tlsCertificateKeyFile="./config/X509-cert-5865884892705360989.pem")
db = Mongo_client.TellDormMeal
data = db.Users

def Get_user():
    output = []
    for s in data.find():
        _id = str(s['_id'])
        output.append({'_id':_id, 'ch_name':s['channel_name'], 'ch_id':s['channel_id']})
    result = []
    for i in range(len(output)):
        result.append(int(output[i]["ch_id"]))
    return result