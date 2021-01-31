import pymongo
import ssl

myclient = pymongo.MongoClient("mongodb+srv://Erkebulan:erkodream@mycluster-klvkf.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

for x in mycol.find({}, {"_id": 0, "name": 1, "address": 1}):
    print(x)