import sqlite3 as sql
import csv
import hashlib

connection = sql.connect('database.db')
cursor = connection.cursor()


# Populate user table
def populate_users(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Users;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Users(username TEXT PRIMARY KEY, password TEXT NOT NULL, email TEXT NOT NULL);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        username = row[0]
        password = row[1]
        email = row[2]
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cursor.execute('INSERT or REPLACE INTO Users (username, password, email) VALUES (?, ?, ?)', (username, hashed_password, email))

    connection.commit()


# Populate caregivers table
def populate_caregivers(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Caregivers;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Caregivers(username TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, code INTEGER);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        username = row[0]
        first_name = row[1]
        last_name = row[2]
        code = row[3]
        cursor.execute('INSERT or REPLACE INTO Caregivers (username, first_name, last_name, code) VALUES (?, ?, ?, ?)', (username, first_name, last_name, code))

    connection.commit()


# Populate patients table
def populate_patients(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Patients;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Patients(username TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, DOB TEXT);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        username = row[0]
        first_name = row[1]
        last_name = row[2]
        dob = row[3]
        cursor.execute('INSERT or REPLACE INTO Patients (username, first_name, last_name, DOB) VALUES (?, ?, ?, ?)', (username, first_name, last_name, dob))

    connection.commit()


# Populate patient data table
def populate_patient_data(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Patient_Data;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Patient_Data(patient TEXT, record_date TEXT, record_time TEXT, readings REAL, comments TEXT, device TEXT,PRIMARY KEY(patient,record_date,record_time));')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        patient = row[0]
        record_date = row[1]
        record_time = row[2]
        readings = row[3]
        comments = row[4]
        device = row[5]
        cursor.execute('INSERT or REPLACE INTO Patient_Data (patient, record_date, record_time, readings, comments, device) VALUES (?, ?, ?, ?, ?, ?)', (patient, record_date, record_time, readings, comments, device))
    connection.commit()


populate_users("Data/User.csv")
populate_patients("Data/Patient.csv")
populate_caregivers("Data/Caregiver.csv")
populate_patient_data("Data/Patient Data.csv")