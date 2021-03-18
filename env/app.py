#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api , reqparse 
from flask_pymongo import PyMongo
import os
import werkzeug
import cv2
import numpy as np



UPLOAD_FOLDER = './assets/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "InformationOfClient"
app.config["MONGO_URI"] = "mongodb://localhost:27017/InformationOfClient"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["IMAGE_UPLOADS"] = "/Users/mai/SeniorProject/flaskwebapi/env/assets/images"

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

# @app.route("/upload-image", methods=["GET", "POST"])
# def upload_image():
   # if request.method == 'POST':
   #      # check if the post request has the file part
   #    if 'file' not in request.files:
   #       #flash('No file part')
   #       return "No file part"
   #    file = request.files['file']
   #      # if user does not select file, browser also
   #      # submit an empty part without filename
   #    if file.filename == '':
   #       return "No selected file"
   #    return redirect(request.url)
   #    if file and allowed_file(file.filename):
   #       filename = secure_filename(file.filename)
   #       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   #       return "uploaaded"
   # return "Success"
   # if request.method == "POST":
   #    if request.files:
   #       image = request.files["image"]
   #       parse.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
         
   #       #image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))                                          
   #       #image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   #       return "Uploaded!"

   # return "Redirect"


@app.route('/addImage',methods=['POST'])
def postImage():

   if request.method == "POST":
      if request.files:
         image = request.files["image"]
         print(image)
         image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

         subprocess.call("python3 detect.py "+ 
        "--source mine/images/new_unknown_"+str(num)+".jpg "+
        "--save-txt --project mine/result "+
        "--name new_unknown_"+str(num)
        ,shell=True)                                          
      return "Saved!"
   return "End processed"
   

        


if __name__ == '__main__':
   # app.run(debug=True,host='0.0.0.0')
   app.run(debug=True)
