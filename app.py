# -- IMPORT SECTION --
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
#from model import checkAuth

# -- INITIALIZATION of APP --
app = Flask(__name__)

# -- CREATION of SECRET KEY for SESSION --
app.secret_key = os.urandom(32)

# -- LOAD ENV VARIABLES from .ENV -- 
load_dotenv()

# -- STORE ENV VARAIBLES --
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# --- DATABASE SETUP -- 
# NAME of DATABASE
app.config['MONGO_DBNAME'] = 'users' 
# URI of DATBASE
app.config['MONGO_URI'] = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.slptq.mongodb.net/users?retryWrites=true&w=majority"
mongo = PyMongo(app)
users = mongo.db.users
curUser = ""

# checks if user is already logged in 
def checkAuth():
    return "username" in session

# -- ROUTES SECTION -- 
@app.route('/')
@app.route('/index')
def index():
    
    if checkAuth(): # if logged in
        curUser = list(users.find({"user": session['username']}))[0]
        return render_template('dashboard.html', user=curUser, message="")
    else: # if not logged in 
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        loginUsers = list(users.find({"user": username}))
        if len(loginUsers) == 0:
            flash("Login failed. Username does not exist.")
            return render_template("login.html", message= "Login failed. Username does not exist.")
        else:
            correctPass = loginUsers[0]['password']
            if password == correctPass: 
                session['username'] = username
                curUser = loginUsers[0]
                return render_template("dashboard.html", user=curUser, message="")
            else: # if password incorrect --> prompt login again 
                return render_template("login.html", message= "Login failed. Password is incorrect.")
    else: 
        return render_template("login.html", message="")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        password = request.form['password']
        repeatPassword = request.form['repeatPassword']
        loginUsers = list(users.find({"user": username}))
        if len(loginUsers) == 1:
            return render_template("signup.html", message= "This username already exists. Please try another!")
        else: 
            if password != repeatPassword: 
                return render_template("signup.html", message="The passwords do not match.")
            else: 
                users.insert({"user": username, "password": password, "firstName": firstName, "lastName": lastName, "expenses":{}})
                return redirect('/login')
    else:
        return render_template("signup.html", message="")


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        toChange = str(request.form.get('category'))
        # print(toChange)
        a = "deposits" + "." + toChange
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
    users.remove({})
    users.insert({"user": "tammy", "password": "yay", "firstName": "Tammy", "lastName": "Chen", "deposits":{"Required Reserves": 400, "Excess Reserves": 100, "Loans": 1000}, 
                    "withdrawls":{"Demand Deposits": 7000, "Other liabilities": 123, "Owner's Equity": 400}})

    #print(loadUsers())
    return "yay"

'''
def loadUsers():
    users = mongo.db.users
    return list(users.find({}))
'''

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')