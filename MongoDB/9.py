import pymongo
import ssl

myclient = pymongo.MongoClient("mongodb+srv://Erkebulan:erkodream@mycluster-klvkf.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

myresult = mycol.find().limit(5)

for x in myresult:
  print(x)