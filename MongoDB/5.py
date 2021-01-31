import pymongo
import ssl

myclient = pymongo.MongoClient("mongodb+srv://Erkebulan:erkodream@mycluster-klvkf.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mydoc = mycol.find({}, {'_id' : 0}).sort("name", -1)

for x in mydoc:
  print(x)