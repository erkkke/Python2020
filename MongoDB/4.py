import pymongo
import ssl

myclient = pymongo.MongoClient("mongodb+srv://Erkebulan:erkodream@mycluster-klvkf.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

myquery = { "address": { "$regex": "^S" } }

for x in mycol.find(myquery):
  print(x)