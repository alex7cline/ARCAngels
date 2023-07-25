import sqlite3 as sql
import hashlib
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.formatters import NumeralTickFormatter

app = Flask(__name__)
app.secret_key = 'ARCBiotracker'
host = 'http://127.0.0.1:5000/'


# Render the login template first
@app.route('/')
def index():
    return render_template('login.html')


# Create route /login to be used to log in
# get username and password fields from form
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
            cursor.execute("SELECT username FROM Users WHERE Users.username=? AND Users.password=?", (username,hashed_password))
        elif user_type == 'Caregiver':
            cursor.execute("SELECT username FROM Users WHERE Users.username=? AND Users.password=?", (username,hashed_password))
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
    if 'username' in session:
        print(session['user_type'])
        if session['user_type'] == 'Patient':
            return render_template('index.html', user=session['username'])
        elif session['user_type'] == 'Caregiver':
            return render_template('index.html', user=session['username'])
    return redirect(url_for('login'))



# prepare some data
#x = [cursor.execute("SELECT timestamp FROM Patient_Data WHERE Patient_data.readings_date=? AND Patient_data=time?", (Date,time))]
#y = [cursor.execute("SELECT readings FROM Patient_Data WHERE Patient_data.readings=?"), (Readings)]



def generate_chart():
    timestamps = ['2023-10-2|2am', '2023-10-3|10pm', '2023-10-4|2pm', '2023-10-5|4pm','2023-10-6|3pm']
    values = [102, 202, 150, 251,100]

    # Create a ColumnDataSource for Bokeh plot
    source = ColumnDataSource(data={'timestamps': timestamps, 'values': values})

    # Create a figure
    p = figure(x_range=timestamps, title="Line Chart with Strings as Data", x_axis_label="Categories", y_axis_label="Values")

    # Plot the data as a line chart
    p.line(x='timestamps', y='values', source=source, line_width=2)
    p.xaxis.major_label_orientation = 45

    # Show the plot
    show(p)

#session['username'] = 'Dog7'

def test():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    # cursor.execute("SELECT record_date,record_time,readings FROM Patient_Data WHERE patient = ?", ('Dog7',))
    # cursor.execute("SELECT * FROM Patient_Data WHERE patient = ?", ('Dog7',))
    cursor.execute("SELECT * FROM Patient_Data")
    user_data = cursor.fetchall()
    print(user_data)



# Run main app
if __name__ == '__main__':
    #app.run()
    #generate_chart()
    test()