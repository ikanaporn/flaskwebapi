#!/usr/bin/env python3
from enum import unique
from flask import Flask,make_response,request,jsonify
import numpy as np
from flask_mongoengine import MongoEngine
import os
from IPython.display import Image
from PIL import Image
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from functools import wraps
import datetime
from bson import ObjectId
import shutil 
import glob
import ntpath
from flask_cors import CORS
from io import BytesIO
import cv2
import requests


app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '*'}})
#CORS(app)


#database_name = "Images"
#database_name = "Clients"
database_name = "API-Detection"
mongodb_password = "Com75591;"

DB_URI = "mongodb+srv://ikanaporn:{}@cluster0.x8seg.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name
)
FOLDER_IMAGE_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/env/assets/images"
FOLDER_FILE_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/env/assets/texts"
FOLDER_YAML_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/"
FOLDER_TRAIN_IMAGE_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/train/images"
FOLDER_TEST_IMAGE_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/test/images"
FOLDER_TRAIN_LABEL_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/train/labels"
FOLDER_TEST_LABEL_UPLOADS = "/Users/mai/SeniorProject/flaskwebapi/test/labels"

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config["MONGODB_HOST"] = DB_URI
app.config["IMAGE_UPLOADS"] = FOLDER_IMAGE_UPLOADS
app.config["FILE_UPLOADS"] = FOLDER_FILE_UPLOADS
app.config["YAML_UPLOADS"] = FOLDER_YAML_UPLOADS
app.config["TRAIN_IMAGE_UPLOADS"] = FOLDER_TRAIN_IMAGE_UPLOADS
app.config["TEST_IMAGE_UPLOADS"] = FOLDER_TEST_IMAGE_UPLOADS
app.config["TRAIN_LABEL_UPLOADS"] = FOLDER_TRAIN_LABEL_UPLOADS
app.config["TEST_LABEL_UPLOADS"] = FOLDER_TEST_LABEL_UPLOADS

db = MongoEngine()
db.init_app(app)

client = MongoClient("mongodb+srv://ikanaporn:{}@cluster0.x8seg.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name
))

deviceCollection = client['device']

url = "http://127.0.0.1:5000/api/info/addTotal"  # request url

headers = {  # headers dict to send in request
  "header_name": "headers_value",
 }

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
   filename = db.StringField(unique=True)
   imgfile = db.ImageField(thumbnail_size=(256,256))
   labelfile = db.FileField()
   identify = db.StringField()
   labeledby = db.StringField()

   def to_json(self):

      return {

         "ids": self.ids,
         "filename": self.filename,
         "imgfile": self.imgfile,
         "labelfile": self.imgfile,
         "identify": self.identify,
         "labeledby": self.labeledby,

      }

      #  Labeled(ids=ids,filename=filename,imgfile=file,labelfile=text,identify=identify,lebeledBy=labededBy)

class Device(db.Document):
   ids = db.StringField(unique=True)
   username = db.StringField(unique=True)
   aType = db.StringField()
   factory = db.StringField(nullable=True)
   password = db.StringField(nullable=True)
   uniqueName = db.StringField(nullable=True)

   def to_json(self):

      return {

         "ids": self.ids,
         "username": self.username,
         "aType": self.aType,
         "factory": self.factory,
         "password": self.password,
         "uniqueName": self.uniqueName,

      }
class Model(db.Document):
   name = db.StringField()
   pathfile = db.StringField()

   def to_json(self):

      return {

         "name": self.name,
         "pathfile": self.pathfile,
      
      }

class Total(db.Document):

   unique_name = db.StringField()
   daily = db.IntField()
   total = db.IntField()
 

   def to_json(self):

      return {
         "unique_name":self.unique_name,
         "daily": self.daily,
         "total": self.total,
        
      }


  

#######AUTHENTICATION########
def token_required(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      token = request.args.get('token') #http://127.0.0.1:5000/routes?token=akdjkjfjfdd

      if not token:
         return jsonify({'message':'Token is missing!'}), 403
      try:
         data = jwt.decode(token, app.config['SECRET_KEY'])
      except:
         return jsonify({'message':'Token is invalid!'}), 403
      
      return f(*args, **kwargs)

   return decorated

@app.route('/api/auth/unprotected')
def unprotected():
   return jsonify({'message':'Anyone can view this!'})

@app.route('/api/auth/protected')
@token_required
def protected():
   return jsonify({'message':'This is only available for people with valid tokens.'})

@app.route('/api/auth/login', methods=['GET', 'POST'])
def login():
   auth = request.authorization

   if not auth or not auth.username or not auth.password:  
      return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

   user = Device.objects.get(username=auth.username)
    
   if check_password_hash(user.password, auth.password):  

      token = jwt.encode({'uniqueName': user.uniqueName, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, app.config['SECRET_KEY'])  
      return jsonify({'token' : token.decode('utf-8')}) 

   return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

   if auth and auth.password == 'password':
      token = jwt.encode({'user':auth.username,'ext':datetime.datetime.utcnow() + datetime.timedalta(minutes=120)}, app.config['SECRET_KEY'])
   
      return jsonify({'token': token.decode('utf-8')})

   return make_response('Could not verify',401,{'API-Authentication':'Basic realm="Login Required"'})


# it's work -  
@app.route('/api/working/image-detect', methods=['POST'])
#@token_required
def api_upload_unknown():
   
   # if 'file' not in request.files:
   #    error = "Missing data source!"
   #    return jsonify({'error': error})
   if request.files:
      print("file is already")
      num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))+1
      file = request.files["image"] 
      #img = Image.open(file.stream)
      #image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      #print("ddd",img)
      #image_sequence = img.getdata()
      #image_array = np.array(image_sequence)
      #print("array np:",image_array)
      #image_avg = np.mean(image_array)
      
      #print("img avg",image_avg)
      filename = "new_unknown_"+str(num)
      time = 0

      file.save(os.path.join(app.config["IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/assets/images/new_unknown_"+str(num)+".jpg"))

      unknown1 = Unknown(ids=num,filename=filename,times=time,file=file)

      unknown1.save()

      return "UnknownImage have been Saved!"
   else:
      return "something wrong!"
   

#labeled upload
@app.route('/api/working/label', methods=['POST','GET'])
@token_required
def api_upload_label():

   num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/texts"))
   
   if request.files:

      identify = request.form["identify"]
      labeledby = request.form["labeledby"]
      file = request.files["image"] 
      text = request.files["text"] 
      
      filename = "labeled_"+str(identify)+"_"+str(num)
      file.save(os.path.join(app.config["IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/assets/images/label_"+str(num)+".jpg"))
      text.save(os.path.join(app.config["FILE_UPLOADS"],"/Users/mai/SeniorProject/flaskwebapi/env/assets/texts/label_"+str(num)+".txt"))
     
      ids = str(num)
      label1 = Labeled(ids=ids,filename=filename,imgfile=file,labelfile=text,identify=identify,labeledby=labeledby)
      label1.save()

      return "Label image have been saved!"
     
   else :
      return "please put a request file."

# @app.route('/api/working/retrain-model', methods=['POST','GET'])
# #@token_required
# def api_retrain_model():
   
#    num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))
   
#    if request.files:
#       if num >= 50 : 
#          file = request.files["yaml"] 
#          file.save(os.path.join(app.config["YAML_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/dataset.yaml"))
         
#          count_train = math.floor((len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/assets/images"))*90)/100)
#          folder_label = os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/train/labels")
         
#          for filename in glob.glob('/Users/mai/SeniorProject/flaskwebapi/env/assets/images/*.jpg')[:count_train-1]: 
#             head, tail = ntpath.split(filename)
#             img = Image.open(filename)
#             img.save(os.path.join(app.config["TRAIN_IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/train/images/"+tail))
         
#          for filename in glob.glob('/Users/mai/SeniorProject/flaskwebapi/env/assets/texts/*.txt')[:count_train-1]: 
#             head, tail = ntpath.split(filename)
#             filename = open(filename,"w")
#             shutil.copyfile('/Users/mai/SeniorProject/flaskwebapi/env/assets/texts/'+tail,'/Users/mai/SeniorProject/flaskwebapi/env/train/labels/'+tail )

#          for filename in glob.glob('/Users/mai/SeniorProject/flaskwebapi/env/assets/images/*.jpg')[count_train:]: 
#             head, tail = ntpath.split(filename)
#             img = Image.open(filename)
#             img.save(os.path.join(app.config["TEST_IMAGE_UPLOADS"], "/Users/mai/SeniorProject/flaskwebapi/env/test/images/"+tail))
      
#          for filename in glob.glob('/Users/mai/SeniorProject/flaskwebapi/env/assets/texts/*.txt')[count_train:]: 
#             head, tail = ntpath.split(filename)
#             filename = open(filename,"w")
#             shutil.copyfile('/Users/mai/SeniorProject/flaskwebapi/env/assets/texts/'+tail,'/Users/mai/SeniorProject/flaskwebapi/env/test/labels/'+tail )
         
#        #  runpy.run_path(file_path='train.py')
#       #run python3 train.py --batch 16 --epochs 50 --data mine/dataset.yaml --weights mine/yolov5s.pt

#       return "YAML file have been saved and train model."

#       else :
#          return "Not enough images, please send more images."

#    else :
#       return "please put a request file."

@app.route('/api/working/retrain-model', methods=['POST','GET'])
@token_required
def api_retrain_model():

   image_path = "/Users/mai/SeniorProject/flaskwebapi/env/assets/images/"
   label_path = "/Users/mai/SeniorProject/flaskwebapi/env/assets/texts/"
   train_path = "/Users/mai/SeniorProject/flaskwebapi/env/train/"
   test_path  = "/Users/mai/SeniorProject/flaskwebapi/env/test/"

   if request:
      identify = request.form["identify"]

      for i in os.listdir(train_path+"images/"):
         os.remove(train_path+"images/"+i)
      for i in os.listdir(train_path+"labels/"):
         os.remove(train_path+"labels/"+i)
      for i in os.listdir(test_path+"images/"):
         os.remove(test_path+"images/"+i)
      for i in os.listdir(test_path+"labels/"):
         os.remove(test_path+"labels/"+i)


      for filename in glob.glob(image_path+'*.jpg')[:]: 
         head, tail = ntpath.split(filename)
         if identify in tail:
               img = Image.open(filename)
               img.save(train_path+"images/"+tail)

      num = len(os.listdir("/Users/mai/SeniorProject/flaskwebapi/env/train/images"))  
      if num >= 50 :
         test_img = []
         import yaml
         article_info = {'train': './train/images', 
                           'val': './test/images',
                           'nc': 1,
                           'names': '[' +identify+ ']'
                           }

         with open(r'/Users/mai/SeniorProject/flaskwebapi/env/dataset.yaml', 'w') as file:
               documents = yaml.dump(article_info, file)

         for filename in glob.glob(label_path+'*.txt')[:]: 
               headlabel, taillabel = ntpath.split(filename)
               if identify in taillabel:
                  filename = open(filename,"w")
                  shutil.copyfile(label_path+taillabel,train_path+'labels/'+taillabel )   

               
         for filename in glob.glob(train_path+"images/"+'*.jpg')[int((len(os.listdir(train_path+"images/"))*90)/100):]: 
               # head, tail = ntpath.split(filename)
               # img = Image.open(filename)
               # img.save(test_path+"images/"+tail)
               # os.remove(filename)
            head, tail = ntpath.split(filename)
            h,t = tail.split(".", 1)
            test_img.append(h)
            img = Image.open(filename)
            img.save(test_path+"images/"+tail)
            os.remove(filename)

         for filename in glob.glob(train_path+"labels/"+'*.txt')[:]: 
               # headlabel, taillabel = ntpath.split(filename)
               # shutil.copyfile(train_path+"labels/"+taillabel,test_path+'labels/'+taillabel )
               # os.remove(filename)
            headlabel, taillabel = ntpath.split(filename)
            h,t = taillabel.split(".", 1)
            if h in test_img:
               shutil.copyfile(train_path+"labels/"+taillabel,test_path+'labels/'+taillabel )
               os.remove(filename)
               
         # run train.py เอาที่ช้างแก้ให้

         return "YAML file have been saved and train model."

      else :
         return "Not enough images, please send more images."

   else :
      return "please put a request file."

# @app.route('/api/working/train-by-identify', methods=['POST','GET'])
# #@token_required
# def api_train_by_identify():
#    if request :
#       identify = request.form["identify"]
#       for i in collection.label :
#          if identify == identify of col.label :
#             #save local floder
#             #if len of local floder == 50 -> run model /
#             #todo - assign - chang
#          else : 
#             #dont have this identify that you spacific.
         
#          #find identify in labeled collection that define identify's row = "glass"
#          #find num that identify's row = "glass" 
#          #if == 50 ->train
#          #else ret ส่งมาอีก x รูปจ้า ยังไม่ครบ


@app.route('/api/test', methods=['GET','POST'])
def api_lebeled():
   return jsonify({'result':"test success."})

@app.route('/api/labeled/<ids>', methods=['POST'])
def api_each_labeled():
   pass

@app.route('/',methods=['GET'])
def hello():
   unknown = Unknown.objects(ids=8)
   return 
   #return "Hello"

@app.route('/api/initiate/register', methods=['POST','GET'])
def api_register():

   data = request.get_json()
   #auth_token = user.encode_auth_token(user.id)
   if data['aType'] == 'iot':
      hashed = generate_password_hash(data['password'], method='sha256')
      uniqueName = str(data['factory']+"_"+data['aType']+"_"+data['ids']+"_")

      newDevice = Device(ids=data['ids'],username=data['username'],aType=data['aType'],factory=data['factory'],password=hashed,uniqueName=uniqueName)
      newDevice.save()

      return "Successfully appied! [ioT]"
     

   elif data['aType'] == 'mobile' :

      newDevice = Device(ids=data['ids'],username="",aType=data['aType'],factory="",password="",uniqueName="")
      newDevice.save()
      
      return "Successfully appied! [mobile]"
   
   else :
      return "Invalid data"
 
@app.route('/api/total', methods=['GET'])
def totallyDevices():
   pass;


@app.route('/api/info/getClient/<uniqueName>', methods=['GET'])
@token_required
def getClient(uniqueName):
   client = Device.objects.get(uniqueName=uniqueName)
   return jsonify({'result':client})
   # return Labeled.query.filter_by(uniqueName=data['uniqueName']).first()

#9.Added model
@app.route('/api/info/addModel', methods=['POST'])
@token_required
def addModel():
   data = request.get_json()

   newModel = Model(name=data['name'],pathfile=data['pathfile'])
   newModel.save()

   return "Successfully model added!"
     
@app.route('/api/info/getAllModel', methods=['GET'])
@token_required
def getAllModel():
   output = []
   for model in Model.objects[:]:
      output.append(model)
   return jsonify({'result':output})

@app.route('/api/info/getOneModel/<name>', methods=['GET'])
@token_required
def getOneModel(name):
   model = Model.objects.get(name=name)
   return jsonify({'result':model})

#10.1Counting
@app.route('/api/info/addTotal', methods=['POST'])
#@token_required
def addTotal():

   total = 0
   for obj in Total.objects[:]:
      x = obj.daily
      total = total + x
      print(total)
      #output.append(total)
   data = request.get_json()
   total = total + data['daily']
   newTotal = Total(unique_name=data['unique_name'],daily=data['daily'],total=total)
   newTotal.save()

   return "Successfully model added!"
    
#10.2Counting
@app.route('/api/info/total/<name>', methods=['GET'])
#@token_required
def getTotal(name):
   output = []
   for obj in Total.objects[:]:
      if (obj.unique_name) == name :
      #  model = Model.objects.get(name=name)
      # return jsonify({'result':model})
         output.append(obj)

   return jsonify({'result':output})


@app.route('/api/working/retrain', methods=['get'])
#@token_required
def retrain():

   output = []
   count = 0

   for obj in Labeled.objects[:] :
      imgfile_id = obj.imgfile._id
      
      filter={
         'files_id': ObjectId(imgfile_id)
      }
      
      result = client['API-Detection']['images.chunks'].find(filter=filter)
     
      for cur in result :
         hexx= cur.buffer.toString('base64')
         print(hexx)


# @app.route('api/addModel',methods=['post'])
# @token_required
# def add_model():

#    pt_path = os.getcwd()+"/api_unknown/model"

#    if request.files:
#       file = request.files["file"]
#       name = request.FILES[file].name
#       file.save(pt_path+"/"+name)
#       return "Your model have been saved."
#    else :
#       return "Please send model file(.pt) again."


#JWT AUTH

#MODEL



if __name__ == '__main__':
   app.run(debug=True)
   #app.run(debug=True,host='http://riorocker97.com/')





