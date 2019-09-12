from flask import Flask, render_template, jsonify, redirect, request
from twilio.twiml.messaging_response import MessagingResponse
from openpyxl import load_workbook, Workbook
import flask_excel as excel
import datetime
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.Users import User
from models.Users import db
import re
from flask import jsonify
import csv
import pandas as pd
import numpy as np
import os
import sys
from flask import Flask,render_template,g,request,flash,redirect,url_for,session,flash
import os
from functools import wraps
import sqlite3


sys.path.insert(1, "PATH TO LOCAL PYTHON PACKAGES")  #OPTIONAL: Only if need to access Python packages installed on a local (non-global) directory
sys.path.insert(2, "PATH TO FLASK DIRECTORY")      #OPTIONAL: Only if you need to add the directory of your flask app


# setup the app
app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
bcrypt = Bcrypt(app)

# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create the db structure
with app.app_context():
    db.create_all()

app.secret_key = os.urandom(24)
app.database='sample.db'
conn=sqlite3.connect('sample.db')


####  setup routes  ####
@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear the inital flash message
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # query the user
    registered_user = User.query.filter_by(username=username).first()

    # check the passwords
    if registered_user is None and bcrypt.check_password_hash(registered_user.password, password) == False:
        flash('Invalid Username/Password')
        return render_template('login.html')

    # login the user
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    email = request.form['email']

    # make sure the password match
    if conf_password != password:
        flash("Passwords do not match")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesnt pass
    if True in check_password.values():
        for k,v in check_password.items():
            if str(v) is "True":
                flash(k)

        return render_template('register.html')

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # create a user, and check if its unique
    user = User(username, pw_hash, email)
    u_unique = user.unique()

    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('login'))

    # else error check what the problem is
    elif u_unique == -1:
        flash("Email address already in use.")
        return render_template('register.html')

    elif u_unique == -2:
        flash("Username already in use.")
        return render_template('register.html')

    else:
        flash("Username and Email already in use.")
        return render_template('register.html')

@app.route("/scrape", methods=['GET'])
def scrape():
    listings = mongo.db.listings
    listings_data = scrape_craigslist.scrape()
    listings.update(
        {},
        listings_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/bootstrap-elements')
def bootstrap_elements():
    return render_template('bootstrap-elements.html', user=current_user)


@app.route('/bootstrap-grid')
def bootstrap_grid():
    return render_template('bootstrap-grid.html', user=current_user)

@app.route('/home')
def home():
    return render_template('home.html', user=current_user)

@app.route('/test')
def hthy():
    return render_template('test.html', user=current_user)

@app.route('/about')
def hthyon():
    return render_template('about.html', user=current_user)

@app.route('/tohelp')
def myththy():
    return render_template('tohelp.html', user=current_user)

@app.route('/base')
def blank_page():
    return render_template('base.html', user=current_user)


@app.route('/agric')
def my_agric():
    return render_template('agric.html', user=current_user)



@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/settings')
def settings():
    return render_template('settings.html', user=current_user)

@app.route('/sef')
def sef():
 return render_template('search.html')

@app.route('/sef1')
def sef1():
 return render_template('search1.html')
@app.route('/del')
def delt():
 return render_template('del.html')

@app.route('/dlt')
def dlt():
 return render_template('dlt.html')

@app.route('/stud', methods=['GET','POST'])
def stud():
 return render_template('agric.html')

@app.route('/coset', methods=['GET','POST'])
def coset():
 return render_template('coset.html')

@app.route('/rec')
def rec(): 
 g.db = connect_db() 
 cur = g.db.execute('select name,reg_num,id_num,year,course from students')
 
 row = cur.fetchall()  
 return render_template('ttt.html',row=row)

@app.route('/cos')
def cos(): 
 g.db = connect_db() 
 cur = g.db.execute('select course_name,abrv from courses')
 
 row = cur.fetchall()  
 return render_template('tt.html',row=row)

@app.route('/rec1')
def rec1(): 
 g.db = connect_db() 
 cur = g.db.execute('select name,reg_num,id_num,year,course from students')
 
 row = cur.fetchall()  
 return render_template('index1.html',row=row)
@app.route('/ser',methods=['POST'])
def ser():
 
 g.db = connect_db()
 cur=g.db.execute( "select * from students where reg_num = ? ", (request.form['search'],) )
 row = cur.fetchall()
 return render_template("ttt.html",row=row)


@app.route('/ser1',methods=['POST'])
def ser1():
 
 g.db = connect_db()
 cur=g.db.execute( "select * from students where reg_num = ? ", (request.form['search'],) )
 row = cur.fetchall()
 return render_template("index1.html",row=row)

@app.route('/delete',methods=['POST'])
def delete():
 g.db = connect_db()
 g.db.execute( "delete from students where reg_num = ? ", (request.form['delete'],) )
 g.db.commit()
 cur=g.db.execute( "select * from students ")
 row=cur.fetchall()
 return render_template("ttt.html",row=row) 


@app.route('/dele',methods=['POST'])
def dele():
 g.db = connect_db()
 g.db.execute( "delete from courses where abrv = ? ", (request.form['dele'],) )
 g.db.commit()
 cur=g.db.execute( "select * from courses ")
 row=cur.fetchall()
 return render_template("tt.html",row=row) 


@app.route('/add', methods=['POST'])
def add():
 g.db=connect_db()
             
 g.db.execute('INSERT INTO students (name,reg_num,id_num,year,course) VALUES(?,?,?,?,?)',[request.form['name'],request.form['reg_num'],request.form['id_num'],request.form['year'],request.form['course']]);
 g.db.commit()
 flash('posted')
 return redirect(url_for('rec'))


@app.route('/addc', methods=['POST'])
def addc():
 g.db=connect_db()
             
 g.db.execute('INSERT INTO courses (course_name,abrv) VALUES(?,?)',[request.form['course_name'],request.form['abrv']]);
 g.db.commit()
 flash('posted')
 return redirect(url_for('cos'))

@app.route('/search')
def search():
 return render_template("search.html")
def connect_db():
 return sqlite3.connect(app.database)

####  end routes  ####


# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# check password complexity
def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        
    """

    # calculating the length
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    ret = {
        'Password is less than 8 characters' : length_error,
        'Password does not contain a number' : digit_error,
        'Password does not contain a uppercase character' : uppercase_error,
        'Password does not contain a lowercase character' : lowercase_error,
        'Password does not contain a special character' : symbol_error,
    }

    return ret



@app.errorhandler(500)
def internal_error(e):
    return render_template('error500.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html')





if __name__ == "__main__":
	# change to app.run(host="0.0.0.0"), if you want other machines to be able to reach the webserver.
	app.run() 