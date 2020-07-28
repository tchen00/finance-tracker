# -- IMPORT SECTION --
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt
from model import *


# -- INITIALIZATION of APP --
app = Flask(__name__)
app.jinja_env.globals.update(formatMoney=formatMoney)

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
        return render_template('intro.html')
        #return redirect('/login')

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
            #correctPass = loginUsers[0]['password']
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), loginUsers[0]['password'].encode('utf-8')) == loginUsers[0]['password'].encode('utf-8'):
                session['username'] = username
                return redirect('/dashboard')
                # return render_template("dashboard.html", user=curUser, message="")
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
                users.insert({"user": username, "password": str(bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()), 'utf-8'), "firstName": firstName, "lastName": lastName, "expenses":{}})
                return redirect('/login')
    else:
        return render_template("signup.html", message="")


@app.route('/update', methods=['GET', 'POST'])
def update():
    if checkAuth(): 
        username = session['username']
        userInfo = list(users.find({"user": username}))[0]
        print(userInfo["deposits"])
        if request.method == "POST":
            toChange = str(request.form.get('category'))
            if toChange in userInfo["deposits"].keys():
                a = "deposits" + "." + toChange
            else: 
                a = "withdrawls" + "." + toChange
            users.update({"user": username}, 
                {"$set": {a: float(request.form['newval']),
                    }})
            return redirect('/dashboard')
        else: 
            return render_template("update.html", user=userInfo)
    else: 
        return redirect('/login')

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

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if checkAuth(): 
        username = session['username']
        userInfo = list(users.find({"user": username}))[0]
        if request.method == "POST":
            title = request.form['title']
            toChange = str(request.form.get('category'))
            a = toChange + "." + title
            users.update({"user": username}, 
                {"$set": {a: float(request.form['amount']),
                    }})
            return redirect('/dashboard')
        else: 
            return render_template("new-entry.html", user=userInfo)
    else: 
        return redirect('/login')

@app.route('/add')
def add():
    users.remove({})
    #users.insert({"user": "tammy", "password": "yay", "firstName": "Tammy", "lastName": "Chen", "deposits":{"Work - May A": 410, "Work - May B": 320, "Allowance": 30}, 
    #               "withdrawls":{"Brunch w/ Friends": 22, "Airpods": 250, "Mini-fan": 19}})

    #print(loadUsers())
    return "yay"

'''
def loadUsers():
    users = mongo.db.users
    return list(users.find({}))
'''

@app.route('/dashboard')
def dashboard(): 
    if checkAuth(): 
        username = session['username']
        userInfo = list(users.find({"user": username}))[0]
        balance = 0
        for i in userInfo["deposits"].values():
            balance += i
        for i in userInfo["withdrawls"].values():
            balance -= i
        return render_template("dashboard.html", user=userInfo, message="", balance = formatMoney(balance))
    else:
        return redirect('/login')

@app.route('/preferences', methods=["GET", "POST"])
def preferences(): 
    if checkAuth(): 
        username = session['username']
        userInfo = list(users.find({"user": username}))[0]
        if request.method == 'POST':
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            user = request.form['username']
            password = request.form['password']
            repeatPassword = request.form['repeatPassword']
            if isEmpty(firstName) and isEmpty(lastName) and isEmpty(user) and isEmpty(password): 
                return render_template("preferences.html", user = userInfo, message="You did not fill in any of the information.")
            if not isEmpty(firstName): 
                users.update({"user": username}, {"$set": {"firstName": firstName,}})
            if not isEmpty(lastName): 
                users.update({"user": username}, {"$set": {"lastName": lastName,}})
            if not isEmpty(user): 
                users.update({"user": username}, {"$set": {"user": user,}})
                session['username'] = user
                username = session['username']
                userInfo = list(users.find({"user": username}))[0]
            if not isEmpty(password) and not isEmpty(repeatPassword): 
                if password != repeatPassword: 
                    return render_template("preferences.html", user = userInfo, message="Passwords do not match.")
                else:
                    users.update({"user": username}, {"$set": {"password": str(bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()), 'utf-8'), }})
            return render_template('dashboard.html', user= userInfo, message="credentials updated")
        else: 
            return render_template("preferences.html", user = userInfo, message="")
    else: 
        return redirect('/login')

@app.route('/logout')
def logout():
    if checkAuth():
        session.pop('username')
        return redirect('/login')
    else: 
        return redirect('/login')



