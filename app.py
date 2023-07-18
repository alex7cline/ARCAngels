
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = 'ARCBiotracker'
host = 'http://127.0.0.1:5000/'


# Render the login template first
@app.route('/')
def index():
    return render_template('login.html')


# Run main app
if __name__ == '__main__':
    app.run()

