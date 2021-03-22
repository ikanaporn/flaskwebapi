#!/usr/bin/env python3
from flask import Flask,make_response,request
from flask_mongoengine import MongoEngine
import os
#from api_constants import mongodb_password


app = Flask(__name__)


database_name = "Images"
mongodb_password = "Com75591;"

DB_URI = "mongodb+srv://ikanaporn:{}@cluster0.x8seg.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name
)
FOLDER_IMAGE_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/env/assets/images"

app.config["MONGODB_HOST"] = DB_URI
app.config["IMAGE_UPLOADS"] = FOLDER_IMAGE_UPLOADS

db = MongoEngine()
db.init_app(app)

class Unknown(db.Document):

   ids = db.IntField()
   filename = db.StringField()
   times = db.IntField()
   file = db.ImageField(thumbnail_size=(256,256))

   def to_json(self):

      return {

         "ids": self.ids,
         "filename": self.filename,
         "times": self.times,
         "file": self.file,

      }
   


class Labeled(db.Document):
   ids = db.StringField()
   filename = db.StringField()
   identify = db.StringField()
   lebeledBy = db.StringField()

   def to_json(self):

      return {

         "ids": self.ids,
         "filename": self.filename,
         "identify": self.identify,
         "lebeledBy": self.lebeledBy,

      }
# it's work -  
@app.route('/api/uploadunknown', methods=['POST'])
def api_upload_unknown():
   if request.files:
      num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
      file = request.files["image"] 
      filename = "new_unknown_"+str(num)
      time = 0

      file.save(os.path.join(app.config["IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/assets/images/new_unknown_"+str(num)+".jpg"))
      
      unknown1 = Unknown(ids=num,filename=filename,times=time,file=file)
      
      unknown1.save()

      return "UnknownImage have been Saved!"


@app.route('/api/dbImages', methods=['POST'])
def db_images():
   lebeled1 = Labeled(ids="0001",filename="mitpol0.png",identify="bottle",lebeledBy="admin1")
   lebeled2 = Labeled(ids="0002",filename="mitpol1.png",identify="bottle",lebeledBy="admin2")
   
   lebeled1.save()
   lebeled2.save()
   return "Created"

@app.route('/api/labeled', methods=['GET','POST'])
def api_lebeled():
   pass

@app.route('/api/labeled/<ids>', methods=['POST'])
def api_each_labeled():
   pass

if __name__ == '__main__':
    app.run(debug=True)







# UPLOAD_FOLDER = './assets/images'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)

# # mongo = PyMongo(app)

# #client = pymongo.MongoClient("mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net")

# client = pymongo.MongoClient("mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net/detect-app?retryWrites=true&w=majority")
# # db = client.test

# # app.config['MONGODB_SETTINGS'] = {
# #     'db': 'Images',
# #     'host': 'cluster0.x8seg.mongodb.net',
# #     'port': 27017
# # }
# # db = MongoEngine()
# # db.init_app(app)


# APP_ROOT = os.path.dirname(os.path.abspath(__file__))



# @app.route('/')
# def home():
#    return "HelLLOO"



# @app.route('/addImage',methods=['POST'])
# def postImage():

#    if request.method == "POST":
#       if request.files:
#          num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
#          image = request.files["image"]
#          print(image)

#          #image_file = args['image']
#          #image_file.save("/Users/mai/SeniorProject/flaskwebapi/env/assets/images/new_unknown_"+str(num)+".jpg")
#          image.save(os.path.join(app.config["IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/assets/images/new_unknown_"+str(num)+".jpg"))
                                      
#       return "Saved!"
   
# @app.route('/upload', methods=['POST'])
# def upload():
#    images_db_table = mongo.db.Images  # database table name
#    if request.method == 'POST':
#       image = request.files["image"]
#       num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
#       #for upload in request.files.getlist("images"): #multiple image handel
#       filename = "new_unknown_"+str(num)+".jpg"
#       images_db_table.insert({'filename': filename})   #insert into database mongo db

#       return 'Image Upload Successfully'

# @app.route('/testpymongo', methods=['POST'])
# def testpymongo():
#    if request.method == 'POST':
#       # image = request.files["image"]
#       # num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
#       # filename = "new_unknown_"+str(num)+".jpg"

#       db = client.Images
#       collection = db.Unknown
#       collection.insert_one({
#          'filename':"01",
#          'type':",jpeg"
#       })
#       return "Test Pymongo Completed!"





# if __name__ == '__main__':
#    # app.run(debug=True,host='0.0.0.0')
#    app.run(debug=True)
