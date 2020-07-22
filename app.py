# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from flask import redirect
from bson import ObjectId

import model

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:hodDWNc250mYoVIT@cluster0.slptq.mongodb.net/users?retryWrites=true&w=majority"

mongo = PyMongo(app)

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return "yip yip"

@app.route('/add')
def add(): 
    # connect to the database
    users = mongo.db.users
    # insert new data
    users.insert({"user": "tammy", "transactions":"n"})
    users.insert({"user": "edward", "transactions":"n"})
    return "yay"