# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask import redirect
from bson import ObjectId
from datetime import datetime

import model

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:hodDWNc250mYoVIT@cluster0.slptq.mongodb.net/users?retryWrites=true&w=majority"

mongo = PyMongo(app)
users = mongo.db.users
curUser = ""

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", time=datetime.now())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginUsers = list(users.find({"user": request.form['username']}))

        if len(loginUsers) > 0:
            curUser = loginUsers[0]
            return render_template("acct_view.html", user=curUser, message="")
        return render_template("index.html", message="Login failed. Please try again.")
    else:
        return ""

@app.route('/update', methods=['GET', 'POST'])
def update():
    return "sample"
    """if request.method == "POST":
        toChange = str(request.form.get('category'))
        print(type(curUser))
        xy = list(users.find({"user": curUser, "assets": toChange}))
        print(x)
        if len(x) == 0:
            xy = list(users.find({"user": curUser, "liabilities": toChange})

        for i in xy:
            print(i)
        x[toChange] = float(request.form["newval"])

        return render_template("acct_view.html", user=curUser, message="Successfully updated.")"""
        
@app.route('/add')
def add():
    # connect to the database

    # overwrite old data with new:
    users.remove({})
    users.insert({"user": "tammy", "assets":{"Required Reserves": 400, "Excess Reserves": 100, "Loans": 1000}, 
                    "liabilities":{"Demand Deposits": 7000, "Other liabilities": 123, "Owner's Equity": 400}})

    print(loadUsers())
    return "yay"

def loadUsers():
    users = mongo.db.users
    return list(users.find({}))