from datetime import datetime
from datetime import timedelta
from email.policy import default
from flask import Flask, redirect, render_template, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from file_storage_helper import FileStorage
import cloudinary
import cloudinary.uploader
from decouple import config

from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
load_dotenv()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mxykwmrfixgxll:19711ff96fa8cea70735297638106ab09d1f595eccc81899d3164d31242458ba@ec2-23-23-151-191.compute-1.amazonaws.com:5432/d9c0t8kfbi1t2k'

app.secret_key= config('SECRET_KEY')
# app.config['IMAGE_UPLOADS'] = r'C:\Users\zinox\Desktop\pyweb\TechWithTim\flask_app\static\images'
app.config['IMAGE_UPLOADS'] = '/tmp/'
app.config["AVATER-FILE"] = ""
app.config["PROFILE_UPLOADED"] = "false"
app.permanent_session_lifetime=timedelta(minutes=2)
db = SQLAlchemy(app)
profile_photo = ""




class Register(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  password = db.Column(db.Text(), nullable=False)
  profile_uploaded = db.Column(db.String(100), nullable = False)
  time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
  
  def __repr__(self):
    return '<Register %r>' % self.name
  
  
class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  author = db.Column(db.String(100), nullable=False)
  email = db.Column(db.Text(), nullable=False)
  author_URL = db.Column(db.Text(), nullable=True)
  post_URL = db.Column(db.Text(), nullable=False)
  title = db.Column(db.String(120), nullable=False)
  category = db.Column(db.String(80), nullable=False)
  post = db.Column(db.Text(), nullable=False)
  time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
  
  def __repr__(self):
    return '<Post %r>' %self.author
  
  
  

@app.route("/register", methods=["POST", "GET"])
def register():
  if request.method == "POST":    
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    repassword = request.form["repassword"]
    if name and email and password and repassword:
      if password != repassword:
        return render_template("register.html", password_error = True)
      if Register.query.filter_by(email=email).first():
        return render_template("register.html", error=True)
      else:
        register = Register(name=name, email=email, profile_uploaded = "False", password=generate_password_hash(password))
        db.session.add(register)
        db.session.commit()
        return redirect("/login")
    
    else:
      return redirect("/register", error=True)
  else:
    if "email" in session:
      return redirect("/dashboard")
    else:
      return render_template("register.html")

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods= ["POST", "GET"])
def login():
  if request.method == 'POST':
 
    email = request.form["email"]
    password = request.form["password"] 
    register_db = Register.query.all()
    for register in register_db:
      if email == register.email:
        if check_password_hash(register.password, password):
        
          session.permanent = True
          session["email"] = email
          register = Register.query.filter_by(email = email).first()
          session["name"] = register.name
          posts = Post.query.order_by(Post.time).all() 
    
          return render_template('dashboard.html', data = session, 
                                   profile_uploaded = app.config["PROFILE_UPLOADED"], 
                                   my_path=app.config["IMAGE_UPLOADS"], file_list =  os.listdir(app.config['IMAGE_UPLOADS']), submitted_posts = posts)
        else:
          return render_template("login.html", password_error = True)
        
    return render_template("login.html", email_error = True)
  else:
    if "email" in session:
      return redirect(url_for('dashboard', view = "home", data=session))
    else:
      return render_template("login.html")
    


@app.route("/dashboard", methods = ["POST", "GET"])
def dashboard():
  storage = FileStorage()
  if request.method == "POST":
    image = request.files["avater-image"]
    if image == "":
      return redirect(request.url)
    profile_photo = secure_filename(image.filename)
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, app.config["IMAGE_UPLOADS"], profile_photo)
    image.save(path)
    
    if Register.query.filter_by(email = session["email"]).first_or_404().profile_uploaded == "False":
      #upload pics     
      storage.uploadProfileURL(path, session["email"]);    
      Register.query.filter_by(email = session["email"]).first_or_404().profile_uploaded = "True"
      db.session.commit()
      #download pics
      storage.downloadProfileURL(app.config["IMAGE_UPLOADS"], session["email"])
      posts = Post.query.order_by(Post.time).all()
      return render_template('dashboard.html', avater_url = profile_photo, 
                           data = session, profile_uploaded = app.config["PROFILE_UPLOADED"], 
                           my_path= app.config["IMAGE_UPLOADS"], file_list =  os.listdir(app.config['IMAGE_UPLOADS']),
                           view = "home", submitted_posts = posts)
    
  else:
    if "email" in session:
      if Register.query.filter_by(email = session["email"]).first().profile_uploaded == "True":
        storage.downloadProfileURL(app.config["IMAGE_UPLOADS"], session["email"])
      posts = Post.query.order_by(Post.time).all()
      reversed(posts)
                
      return render_template('dashboard.html', data = session, 
                                   profile_uploaded = app.config["PROFILE_UPLOADED"], 
                                   my_path=app.config["IMAGE_UPLOADS"], file_list =  os.listdir(app.config['IMAGE_UPLOADS']), submitted_posts = posts)
    else:
      return redirect("/login")


@app.route("/dashboard/logout")
def logout():
  session.pop("email", None)
  session.pop("name", None)
  
  return render_template("login.html")

@app.route("/dashboard/post", methods=["POST", "GET"])
def post():
  
  if request.method == "POST":
    image = request.files["image-input"]
    if image == "":
      return redirect(request.url)
    #upload_image_here
    #redirect to the post page where the post will be rendered
    
    profile_photo = secure_filename(image.filename)
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, app.config["IMAGE_UPLOADS"], profile_photo)
    image.save(path)
    
    author = session["name"]
    email = session["email"]
    author_URL = app.config['IMAGE_UPLOADS'] + "/"+ session["email"]+".jpg"
    post_URL = app.config['IMAGE_UPLOADS']+"/"+image.filename
    title = request.form["title"]
    category = request.form['category']
    post = request.form['post']
    
    uploadPostImage(author, email, author_URL, post_URL, title, category, post)

  else:
    ...
    # if Register.query.filter_by(email = session["email"]).first_or_404().profile_uploaded == "True":
    #   storage.downloadProfileURL(app.config["IMAGE_UPLOADS"], session["email"])
      
  return render_template('dashboard.html', data = session, view="post",
                                   profile_uploaded = app.config["PROFILE_UPLOADED"], 
                                   my_path=app.config["IMAGE_UPLOADS"], file_list =  os.listdir(app.config['IMAGE_UPLOADS']))
      

@app.route("/dashboard/details/<title>/<post>", methods=["POST", "GET"])
def details(title, post):
  if request.method == 'GET':
     return render_template('details.html', data = session, view="post",
                                   profile_uploaded = app.config["PROFILE_UPLOADED"], 
                                   my_path=app.config["IMAGE_UPLOADS"],
                                   file_list =  os.listdir(app.config['IMAGE_UPLOADS']), 
                                   title=title, post=post)

def checkPasswordValidity(password, repassword):
  if password == repassword:
    return True
  return False

def uploadPostImage(author, email, author_URL, post_URL, title, category, post):

  cloudinary.config(cloud_name = config('CLOUD_NAME'), api_key= config('API_KEY'), 
    api_secret= config('API_SECRET'))
  # cloudinary.config(cloud_name = os.geten)
  post_image = cloudinary.uploader.upload(post_URL)
  author_image = cloudinary.uploader.upload(author_URL)
  savePostImageURL(author, email, author_image.get('secure_url'),
                   post_image.get('secure_url'), title, category, post)
  
  
def savePostImageURL(author, email, author_URL, post_URL, title, category, post):
  post = Post(author= author, email=email, author_URL = author_URL, 
                post_URL = post_URL, title = title, category = category,post=post)
  db.session.add(post)
  db.session.commit()
  posts = Post.query.order_by(Post.time).all()
  reversed(posts)
  print("The New Post has been saved")
  return redirect(url_for('dashboard', data = session, 
                                   profile_uploaded = app.config["PROFILE_UPLOADED"], 
                                   my_path=app.config["IMAGE_UPLOADS"], file_list =  os.listdir(app.config['IMAGE_UPLOADS']), view="home", submitted_posts = posts))
  

if __name__ == "__main__":
  app.run(debug = True)