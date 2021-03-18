#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "InformationOfClient"
app.config["MONGO_URI"] = "mongodb://localhost:27017/InformationOfClient"

mongo = PyMongo(app)

@app.route('/')
def home():
   return "HelLLOO"

@app.route('/viewInformation',methods=['GET'])
def getInformationList():
   infoList = mongo.db.information
   InformationOfClient = []
   info = information.find()
   for j in info:
      j.pop('informations')
      InformationOfClient.append(j)
   return jsonify(InformationOfClient)



if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')
