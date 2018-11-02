from flask import Flask, render_template,url_for,request,session,redirect
from hashlib import sha256
import os
app=Flask(__name__)
app.config['SECRET_KEY']=b'N\x83Y\x99\x04\xc9\xcfI\xb7\xfc\xce\xd1\xcf\x01\xa8\xccr\xbb&\x1b\x11\xac\xc7V'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)
