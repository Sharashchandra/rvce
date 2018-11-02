from flask import Flask, render_template,url_for,request,session,redirect
from hashlib import sha256
from pymongo import MongoClient
app=Flask(__name__)
app.config['SECRET_KEY']=b'N\x83Y\x99\x04\xc9\xcfI\xb7\xfc\xce\xd1\xcf\x01\xa8\xccr\xbb&\x1b\x11\xac\xc7V'

#Configuring mongodb
client = MongoClient()
db = client['rvce']
users = db.users



db_entries = {"name" : "", "email" : "", "password" : "", "category" : "", "entity_name" : "", "entity_location" : "", "capacity" : 0}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/category")
def category():
    return render_template('category.html')

@app.route("/details")
def details():
    return render_template('details.html')

@app.route("/signup")
def signup():
    stuff = {"name" : "", "location":"1234567890", "Capacity":"5"}
    users.insert_one(stuff).inserted_id
    return render_template("owner_form.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/addowner")
def addowner():
    name = request.form['Name']
    location = request.form['Location']
    capacity = request.form['Capacity']
    category = request.form['Category']

@app.errorhandler(404)
def not_found():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)
