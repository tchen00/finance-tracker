# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
#from model import checkAuth

# -- Initialization section --
app = Flask(__name__)

#creates secret key for sessions
app.secret_key = os.urandom(32)

# first load env variable 
load_dotenv()

# stores env variable with new names 
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.slptq.mongodb.net/users?retryWrites=true&w=majority"

mongo = PyMongo(app)
users = mongo.db.users
curUser = ""

def checkAuth():
    return "username" in session

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    if checkAuth(): # if logged in
        curUser = list(users.find({"user": session['username']}))[0]
        return render_template('dashboard.html', user=curUser, message="")
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        loginUsers = list(users.find({"user": username}))
        print(loginUsers)
        if len(loginUsers) == 0:
            flash("Login failed. Username does not exist.")
            return render_template("login.html", message= "Login failed. Username does not exist.")
        else: 
            correctPass = loginUsers[0]['password']
            if password == correctPass: 
                session['username'] = username
                curUser = loginUsers[0]
                return render_template("dashboard.html", user=curUser, message="")
            else: 
                return render_template("login.html", message= "Login failed. Password is incorrect.")
    else:
        return render_template("login.html", message="")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeatPassword = request.form['repeatPassword']
        loginUsers = list(users.find({"user": username}))
        if len(loginUsers) == 1:
            return render_template("signup.html", message= "This user already exists. Please try another!")
        else: 
            if password != repeatPassword: 
                return render_template("signup.html", message="The passwords do not match.")
            else: 
                users.insert({"user": username, "password": password, "expenses":{}})
                return redirect('/login')
    else:
        return render_template("signup.html", message="")


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        toChange = str(request.form.get('category'))
        print(toChange)
        a = "assets" + "." + toChange
        users.update({"user": "tammy"}, 
            {"$set": {a: float(request.form['newval']),
                }})
        return "yay"
        '''
        print(type(curUser))
        xy = list(users.find({"user": curUser, "assets": toChange}))
        print(x)
        if len(x) == 0:
            xy = list(users.find({"user": curUser, "liabilities": toChange})

        for i in xy:
            print(i)
        x[toChange] = float(request.form["newval"])

        return render_template("dashboard.html", user=curUser, message="Successfully updated.")
        '''
        
@app.route('/add')
def add():
    # connect to the database

    # overwrite old data with new:
    users.remove({})
    users.insert({"user": "tammy", "password": "yay", "assets":{"Required Reserves": 400, "Excess Reserves": 100, "Loans": 1000}, 
                    "liabilities":{"Demand Deposits": 7000, "Other liabilities": 123, "Owner's Equity": 400}})

    print(loadUsers())
    return "yay"

def loadUsers():
    users = mongo.db.users
    return list(users.find({}))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')