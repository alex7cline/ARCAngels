import sqlite3 as sql
import hashlib
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = 'ARCBiotracker'
host = 'http://127.0.0.1:5000/'


# Render the login template first
@app.route('/')
def index():
    return render_template('login.html')


# Create route /login to be used to log in to Lion Auction
# get email and password fields from form
# hash password and search users database
# if the user info is found create a session
# if the user info is incorrect add message to index template
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        username = request.form['Username']
        password = request.form['Password']
        user_type = request.form['user_type']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user_type == 'Patient':
            cursor.execute("SELECT username FROM Users WHERE Users.username=?", username)
        elif user_type == 'Caregiver':
            cursor.execute("SELECT username FROM Users WHERE Users.username=?", username)
        user = cursor.fetchone()
        print(user)
        print(user_type)
        if user is not None:
            session['username'] = user[0]
            session['user_type'] = user_type
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


# This path verifies if a user is logged in and returns the home page
# If the user is not logged in, they are redirected to the login page
@app.route('/home')
def home():
    if 'email' in session:
        print(session['user_type'])
        if session['user_type'] == 'Patient':
            return render_template('index.html', user=session['username'])
        elif session['user_type'] == 'Caregiver':
            return render_template('index.html', user=session['username'])
    return redirect(url_for('login'))


# Run main app
if __name__ == '__main__':
    app.run()

