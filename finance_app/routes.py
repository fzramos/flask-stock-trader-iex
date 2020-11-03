from finance_app import app
from flask import render_template, redirect, url_for
from finance_app.forms import UserInfoForm, LoginForm
from flask_login import login_required, login_user, current_user, logout_user

@app.route('/')
def home():
    # if not current_user.is_authenticated:
    #     return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = UserInfoForm()

    # if request.method == 'POST':
    #     company

    return render_template('register.html', form = form)
    # return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)
    # return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('register'))
