import os
import pyrebase
import cloudinary as Cloud




class FileStorage:
  
  config = {
  "apiKey": "AIzaSyASyn4_3tViKDdkp-zCsUgVaIxJcBiFiOU",
  "authDomain": "poster-f8926.firebaseapp.com",
  "projectId": "poster-f8926",
  "storageBucket": "poster-f8926.appspot.com",
  "messagingSenderId": "58754244570",
  "appId": "1:58754244570:web:3ba9f5a518547d30f56ae3",
  "measurementId": "G-RW7H49MGM8",
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