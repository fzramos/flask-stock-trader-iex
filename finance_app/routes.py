from finance_app import app, db
from flask import render_template, redirect, url_for, request
from finance_app.forms import UserInfoForm, LoginForm, QuoteForm, BuyForm, SellForm
from finance_app.models import User, Company, Transact, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from iexfinance.stocks import Stock
# to allow for Sql sum of column values
from sqlalchemy import func

# route to make sure no cookies are saved (so you dont have to do ctrl + F5 every time)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# transact = Transact.query.filter ( user_id = current_user.id )


# returnrender_template ( 'index.html', transactions = transact)
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))

    current_stocks = db.session.query(
        Company.symbol,
        Company.name,
        func.sum(Transact.shares).label('shares_sum')
    ).join(Transact.business
    ).filter(Transact.user_id == current_user.id
    ).group_by(Transact.company_id
    ).having(func.sum(Transact.shares) > 0
    ).all()

    portfolio = dict()
    for value in current_stocks:
        
        # so stocks that you sold off in the past don't show up
        # if value.shares_sum <= 0:
        #     continue
        stock = Stock(value.symbol)
        current_price = stock.get_quote()['latestPrice']

        portfolio[value.symbol] = {
            'name': value.name,
            'shares_sum': value.shares_sum,
            'price': current_price,
            'total_price': current_price * value.shares_sum
        }

    return render_template('index.html', portfolio = portfolio)

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
        else:
            return render_template('failure.html', msg = f"{symbol} is not recognized as a valid stock symbol.")
    return render_template('quote.html', form = form)

@app.route('/buy', methods = ['GET', 'POST'])
@login_required
def buy_stock():
    form = BuyForm()
    if request.method == 'POST' and form.validate():
        # return render_template('failure.html', msg = 'finally')
        symbol = form.symbol.data.upper()
        shares = form.shares.data
        # company = Company.query.filter_by(symbol = symbol)
        company = Company.query.filter(Company.symbol == symbol).first()
        if company:
            
            stock = Stock(company.symbol)
            current_price = stock.get_quote()['latestPrice']
            price_each_cent = int(current_price * 100)
            cost_cent = price_each_cent * shares
            cost = cost_cent / 100
            if cost_cent > current_user.cash_cent:
                return render_template('failure.html',\
                    msg = f'The cost of these shares, {cost:.2f}, is '\
                    + f'more than the cash you have in your account, '\
                    + f'{current_user.cash_cent /100}.')
            current_user.cash_cent -= cost_cent
            user_id = current_user.id

            transact = Transact(shares, price_each_cent, user_id, company.id)

            db.session.add(transact)
            db.session.commit()

            return redirect(url_for('home'))
        else:
            return render_template('failure.html', msg = f'{symbol} is not a recognized stock symbol.')
    return render_template('buy.html', form = form)

# history next
@app.route('/history')
@login_required
def history():
    user_history = db.session.query(
        Company.symbol,
        Transact.shares,
        Transact.price_each_cent,
        Transact.time
    ).join(Transact.business
    ).filter(Transact.user_id == current_user.id
    ).all()

    return render_template('history.html', transactions = user_history)


@app.route('/sell', methods = ['GET', 'POST'])
@login_required
def sell_stock():
    form = SellForm()

    current_stocks = db.session.query(
        Company.symbol,
        Company.id,
        func.sum(Transact.shares).label('shares_sum')
    ).join(Transact.business
    ).filter(Transact.user_id == current_user.id
    ).group_by(Transact.company_id
    ).having(func.sum(Transact.shares) > 0
    ).all()

    portfolio = dict()
    for value in current_stocks:
        # be careful!! key positional stuff in dict
        portfolio[value.symbol] = [value.shares_sum, value.id]
    
    # attempting to dynamically add the user's owned stock symbols to the drop down
    for key in portfolio.keys():
        form.symbol.choices.append((key, key))

    if request.method == 'POST' and form.validate():
        sell_sym = form.symbol.data
        sell_shares = form.shares.data

        if sell_shares <= portfolio[sell_sym][0]:

            # getting company of symbol for company id
            # maybe make more efficient with backref? since we 
            # have the symbol, just not id
            # company = Company.query.filter(Company.symbol == sell_sym).first()
            company_id = portfolio[sell_sym][1]

            stock = Stock(sell_sym)
            current_price = stock.get_quote()['latestPrice']
            price_each_cent = int(current_price * 100)
            cost_cent = price_each_cent * sell_shares
            current_user.cash_cent += cost_cent
            user_id = current_user.id

            transact = Transact(-sell_shares, price_each_cent, user_id, company_id)

            db.session.add(transact)
            db.session.commit()

            return redirect(url_for('home'))
        else:
            return render_template('failure.html',\
                msg = f'You do not own {sell_shares} shares of {sell_sym}. '\
                + f'You own {portfolio[sell_sym][0]} {sell_sym} stocks.')
            render_template('fail')

    return render_template('sell.html', form = form, portfolio = portfolio)