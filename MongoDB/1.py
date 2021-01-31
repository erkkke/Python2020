import pymongo
import ssl

client = pymongo.MongoClient("mongodb+srv://Erkebulan:erkodream@mycluster-klvkf.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)

print(client.list_database_names())

mydb = client["mydatabase"]
mycol = mydb["students"]

print(mydb.list_collection_names())

mydict = {'name': "Askar", 'surname' : "Akshabayev", 'id' : "04BD"}
x = mycol.insert_one(mydict)