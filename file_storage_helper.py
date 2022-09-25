import os
import pyrebase
import cloudinary as Cloud
from decouple import config



class FileStorage:
  
  config = {
  "apiKey": config('firebase_apiKey'),
  "authDomain": config('firebase_authDomain'),
  "projectId": config('firebase_projectId'),
  "storageBucket": config('firebase_storageBucket'),
  "messagingSenderId": config('firebase_messagingSenderId'),
  "appId": config('firebase_appId'),
  "measurementId": config('firebase_measurementId'),
   "databaseURL" : ""
   }
 
  
  firebase = pyrebase.initialize_app(config)
  

  def __init__(self):
    # self.auth
    ...
    
  def uploadProfileURL(self, file_path, user_email):
    storage = self.firebase.storage()
    storage.child("profile_pictures/" + user_email + ".jpg").put(file_path)
    # storage.child("profile_pictures")   
    
  def downloadProfileURL(self, saving_path, user_email):
    storage = self.firebase.storage()
    storage.child("profile_pictures/" + 
                  user_email + ".jpg").download(path="gs://poster-f8926.appspot.com/", 
                                                filename=saving_path + "/" + user_email + ".jpg")           

 
    
    ...