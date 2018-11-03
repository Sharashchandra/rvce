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

visit = False

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/list_banks")
def list_banks():
    return render_template('list_banks.html')


@app.route("/list_rest")
def list_rest():
    return render_template('list_rest.html')

@app.route("/list_govt")
def list_govt():
    return render_template('list_govt.html')   

@app.route("/details")
def details():
    return render_template('details.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        db_entries["name"] = request.form['Name']
        db_entries["email"] = request.form['email']
        db_entries["password"] = sha256(request.form['pwd'].encode()).hexdigest()
        users.insert_one(db_entries)
        return redirect(url_for('signin'))
    return render_template("signup.html")


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        emailin = request.form['email']
        passwordin = request.form['password']
        result = users.find_one({"email" : emailin})
        if sha256(passwordin.encode()).hexdigest() == result['password']:
            return redirect(url_for('addowner'))
        return render_template('signin.html')
    return render_template("signin.html")

@app.route("/addowner", methods=['GET', 'POST'])
def addowner():
    visit = True
    if request.method == 'POST':
        entity_name = request.form['Entity_Name']
        location = request.form['Location']
        capacity = request.form['Capacity']
        category = request.form['Category']
        return redirect(url_for("/addowner"))
    return render_template("owner_form.html", visit=visit)

@app.route("/final")
def final():
    visit = True
    return render_template("final.html")

@app.errorhandler(404)
def not_found():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)
