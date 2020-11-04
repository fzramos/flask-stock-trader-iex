from finance_app import app, db
from flask import render_template, redirect, url_for, request
from finance_app.forms import UserInfoForm, LoginForm, QuoteForm
from finance_app.models import User, Company, Transact, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from iexfinance.stocks import Stock

# route to make sure no cookies are saved (so you dont have to do ctrl + F5 every time)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))

    
    
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = UserInfoForm()

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        print(username, password)

        user = User(username, password)

        db.session.add(user)
        db.session.commit()

        # Should this work or make it harder to loggin/meet some type of criteria
        logged_user = User.query.filter(User.username == username).first()
        login_user(logged_user)

        return redirect(url_for('home'))

    return render_template('register.html', form = form)
    # return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        logged_user = User.query.filter(User.username == username).first()

        if logged_user and check_password_hash(logged_user.hash, password):
            login_user(logged_user)
            return redirect(url_for('home'))


    return render_template('login.html', form = form)
    # return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))

@app.route('/quote', methods = ['GET', 'POST'])
@login_required
def quote():
    form = QuoteForm()

    if request.method == 'POST' and form.validate():
        symbol = form.symbol.data.upper()
        # check if inputed symbol in symbol table
        company = Company.query.filter(Company.symbol == symbol).first()

        if company:
            stock = Stock(company.symbol)
            current_price = stock.get_quote()['latestPrice']
            print(current_price)

            # use api and symbol to get stock current price and pass it to quoted
            # return redirect(url_for('quoted')) i think this is too much
            return render_template('quoted.html', company = company, price = current_price) # include company name, symbol and current price in pass

    return render_template('quote.html', form = form)

