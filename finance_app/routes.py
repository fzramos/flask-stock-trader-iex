from finance_app import app
from flask import render_template, redirect

@app.route('/')
def home():
    # if not login:
    #     return redirect('/login')
    return render_template('index.html')