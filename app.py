import sqlite3 as sql
import hashlib
from flask import Flask, render_template, request, session, redirect, url_for
from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

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


@app.route('/sign-up', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        username = request.form['uname']
        password = request.form['pass']
        email = request.form['email']
        first_name = request.form['fname']
        last_name = request.form['lname']
        dob = request.form['DOB']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cursor.execute("SELECT username FROM Users WHERE Users.username=?", (username,))
        user = cursor.fetchone()
        if user is not None:
            return render_template('signUp.html', message='Username already taken')
        else:
            cursor.execute('INSERT INTO Users (username, password,email) VALUES (?, ?, ?)', (username, hashed_password,email))
            cursor.execute('INSERT INTO Patients (username,first_name, last_name, DOB) VALUES (?, ?, ?, ?)', (username, first_name,last_name,dob))
            connection.commit()
            return render_template('login.html', success='Successfully Created Account')
    return render_template('signUp.html')


@app.route('/view-readings')
def viewreadings():
    if session['user_type'] == 'Patient':
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT record_date,record_time,readings FROM Patient_Data WHERE patient = ?", (session['username'],))
        user_data = cursor.fetchall()
        if (user_data):
            # Generate the Bokeh plot
            chart = generate_patient_chart(session['username'])
            # Get the JavaScript and HTML components of the Bokeh plot
            script, div = components(chart)
            # Pass Bokeh plot components to the template context
            return render_template('chart.html', user=session['username'], bokeh_script=script, bokeh_div=div)
        return render_template('chart.html', user=session['username'], message="No Data to Display")
    else:
        return render_template('index.html', user=session['username'])


@app.route('/add-data', methods=['POST', 'GET'])
def adddata():
    if request.method == 'POST':
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        reading_date = request.form['readingdate']
        reading_time = request.form['time']
        reading = request.form['reading']
        notes = request.form['Notes']
        device = request.form['device']
        cursor.execute('INSERT OR REPLACE INTO Patient_Data (patient,record_date,record_time,readings,comments,'
                       'device) VALUES (?, ?, ?, ?, ?, ?)', (session['username'], str(reading_date),str(reading_time),reading,notes,device))
        connection.commit()
        return render_template('addData.html', success='Successfully Added Data')
    return render_template('addData.html')


# This route ends the users current session and redirects them to the login page
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect('/')


def generate_chart(timestamps, readings):

    # Create a ColumnDataSource for Bokeh plot
    source = ColumnDataSource(data={'timestamps': timestamps, 'readings': readings})
    # Create a figure
    p = figure(x_range=timestamps, title="Your Glucose Readings", x_axis_label="Day & Time", y_axis_label="Readings (mg/dL)")

    # Plot the data as a line chart
    p.line(x='timestamps', y='readings', source=source, line_width=2)
    p.xaxis.major_label_orientation = 45
    # Set the y-axis range to auto
    p.y_range = p.y_range if p.y_range is None else p.y_range
    p.y_range.start = min(readings)
    p.y_range.end = max(readings)
    p.y_range.flipped = True
    # Show the plot
    # show(p)
    return p


# Connect to database and pull record_date, record_time, and readings from patient data that matches the signed in patient
def generate_patient_chart(patient):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT record_date,record_time,readings FROM Patient_Data WHERE patient = ?", (patient,))
    user_data = cursor.fetchall()
    date_time = []
    readings = []
    for tuple in user_data:
        record_date = tuple[0]
        record_time = tuple[1]
        reading = tuple[2]
        date_time.append(record_date + ' ' + record_time)
        readings.append(reading)
    # print(date_time)
    # print(readings)
    chart = generate_chart(date_time, readings)
    return chart


# Run main app
if __name__ == '__main__':
    app.run()
