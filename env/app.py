#!/usr/bin/env python3
from flask import Flask, request, jsonify, url_for
import pymongo
import os




UPLOAD_FOLDER = './assets/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# # app.config["MONGO_URI"] = "mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net/Images?retryWrites=true&w=majority"
# app.config["MONGO_URI"] = "mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net/detect-app?retryWrites=true&w=majority"
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["IMAGE_UPLOADS"] = "/Users/mai/SeniorProject/flaskwebapi/env/assets/images"

# mongo = PyMongo(app)

#client = pymongo.MongoClient("mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net")

client = pymongo.MongoClient("mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net/detect-app?retryWrites=true&w=majority")
# db = client.test

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'Images',
#     'host': 'cluster0.x8seg.mongodb.net',
#     'port': 27017
# }
# db = MongoEngine()
# db.init_app(app)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/')
def home():
   return "HelLLOO"



@app.route('/addImage',methods=['POST'])
def postImage():

   if request.method == "POST":
      if request.files:
         num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
         image = request.files["image"]
         print(image)

         #image_file = args['image']
         #image_file.save("/Users/mai/SeniorProject/flaskwebapi/env/assets/images/new_unknown_"+str(num)+".jpg")
         image.save(os.path.join(app.config["IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/assets/images/new_unknown_"+str(num)+".jpg"))
                                      
      return "Saved!"
   
@app.route('/upload', methods=['POST'])
def upload():
   images_db_table = mongo.db.Images  # database table name
   if request.method == 'POST':
      image = request.files["image"]
      num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
      #for upload in request.files.getlist("images"): #multiple image handel
      filename = "new_unknown_"+str(num)+".jpg"
      images_db_table.insert({'filename': filename})   #insert into database mongo db

      return 'Image Upload Successfully'

@app.route('/testpymongo', methods=['POST'])
def testpymongo():
   if request.method == 'POST':
      # image = request.files["image"]
      # num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
      # filename = "new_unknown_"+str(num)+".jpg"

      db = client.Images
      collection = db.Unknown
      collection.insert_one({
         'filename':"01",
         'type':",jpeg"
      })
      return "Test Pymongo Completed!"





if __name__ == '__main__':
   # app.run(debug=True,host='0.0.0.0')
   app.run(debug=True)
