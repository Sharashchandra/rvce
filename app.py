from flask import Flask, render_template,url_for,request,session,redirect
from hashlib import sha256
from pymongo import MongoClient
app=Flask(__name__)
app.config['SECRET_KEY']=b'N\x83Y\x99\x04\xc9\xcfI\xb7\xfc\xce\xd1\xcf\x01\xa8\xccr\xbb&\x1b\x11\xac\xc7V'

client = MongoClient()

db = client['rvce']
users = db.users


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
    stuff = {"name" : "Something", "contact_no":"1234567890"}
    users.insert_one(stuff).inserted_id
    return "<h1>Something</h1>"

@app.route("/signin")
def signin():
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)
