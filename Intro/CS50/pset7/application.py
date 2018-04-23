import hashlib
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, Markup
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """Home page!"""
    # GET
    return render_template("index.html")

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions."""
    # POST
    if request.method == "POST":
        # delete current and create a new history table
        db.execute("DROP TABLE :table_name", table_name=session["h_table"])
        db.execute("CREATE TABLE :table_name ('date_time' TEXT PRIMARY KEY, 'name' TEXT, 'symbol' TEXT, 'trans_type' TEXT,"
                   "'price' TEXT, 'amount' INTEGER, 'balance_change' TEXT)", table_name=session["h_table"])

        # success
        flash("History cleared!")
        return redirect(url_for('history'))

    # GET
    rows=db.execute("SELECT * FROM :table_name", table_name=session["h_table"])
    if len(rows) != 0:
        return render_template("history.html", rows=rows)
    else:
        return render_template("history.html")

@app.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():

    # POST
    if request.method == "POST":
        """Complete purchase request"""
        # details from previous pages
        (amount, cost, new_balance) = session["purchase_details"]       # int, float, float
        (name, price, symbol) = session["stock_info"]                   # string, usd(float), string
        balance = session["balance"]                                    # usd(float)

        # get current date and time (base time zone will be UTC)
        date_time = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")

        # check for existing stock with matching name/symbol
        rows = db.execute("SELECT * FROM :table_name WHERE name=:NAME AND symbol=:SYMBOL", table_name=session["p_table"],
                          NAME=name, SYMBOL=symbol)

        # update stock portfolio table
        if len(rows) == 0:
            db.execute("INSERT INTO :table_name ('name', 'symbol', 'amount') VALUES(:NAME, :SYMBOL, :AMOUNT)",
                        table_name=session["p_table"], NAME=name, SYMBOL=symbol, AMOUNT=amount)
        else:
            db.execute("UPDATE :table_name SET amount=:AMOUNT WHERE name=:NAME AND symbol=:SYMBOL",
                        table_name=session["p_table"], AMOUNT=amount+rows[0]["amount"], NAME=name, SYMBOL=symbol)

        # log recent purchase into history table
        db.execute("INSERT INTO :table_name ('date_time', 'name', 'symbol', 'trans_type', 'price', 'amount', 'balance_change')"
                   "VALUES(:DATE_TIME, :NAME, :SYMBOL, :TRANS_TYPE, :PRICE, :AMOUNT, :BALANCE_CHANGE)", table_name=session["h_table"],
                   DATE_TIME=date_time, NAME=name, SYMBOL=symbol, TRANS_TYPE="Purchase", PRICE=price, AMOUNT=amount,
                   BALANCE_CHANGE="-"+usd(cost))

        # update user's balance
        db.execute("UPDATE 'users' SET balance=:BALANCE WHERE id=:ID", BALANCE=usd(new_balance), ID=session["user_id"])
        session["balance"] = usd(new_balance)

        # clear session details
        session["purchase_details"] = None
        session["stock_info"] = None

        flash("Stock purchased!")
        return redirect(url_for("portfolio"))

    # GET
    else:
        return redirect(url_for("quote"))

@app.route("/porfolio", methods=["GET", "POST"])
@login_required
def portfolio():
    """Display stock portfolio."""
    # GET
    if request.method == "GET":

        # get stock portfolio for current user
        rows = db.execute("SELECT * FROM :table_name", table_name=session["p_table"])

        # insert current price per share into each row of rows
        for i in range(0, len(rows)):
            rows[i]['price'] = usd(lookup(rows[i]['symbol'])[1])

        return render_template("portfolio.html", num=len(rows), rows=rows)

    # POST
    """Stock liquidation confirmation."""
    # import variables          #   string        string            usd(float)             int          usd(float)
    data = session["data"]      # [stock name, stock symbol, current price per share, amount to sell, monetary gain]

    # update stock portfolio table
    for i in range(0, len(data)):
        # get current number of stocks owned
        row = db.execute("SELECT * FROM :table_name WHERE symbol = :SYMBOL", table_name=session["p_table"], SYMBOL=data[i][1])
        owned = row[0]["amount"]
        db.execute("UPDATE :table_name SET amount = :AMOUNT where symbol = :SYMBOL", table_name=session["p_table"],
                    AMOUNT=owned-data[i][3], SYMBOL=data[i][1])
        # delete entry from portfolio table if 0 shares are owned
        row = db.execute("SELECT * FROM :table_name WHERE symbol = :SYMBOL", table_name=session["p_table"], SYMBOL=data[i][1])
        if row[0]["amount"] == 0:
            db.execute("DELETE FROM :table_name WHERE symbol=:SYMBOL", table_name=session["p_table"], SYMBOL=data[i][1])

    # update user balance and session variable
    db.execute("UPDATE users SET balance = :new_balance WHERE id=:ID", new_balance=usd(session["new_balance"]),
                ID=session["user_id"])
    session["balance"] = usd(session["new_balance"])

    # get current date and time (base time zone will be UTC)
    date_time = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")

    # log recent transaction(s) into history table
    for i in range(0, len(data)):
        db.execute("INSERT INTO :table_name ('date_time', 'name', 'symbol', 'trans_type', 'price', 'amount', 'balance_change')"
                   "VALUES(:DATE_TIME, :NAME, :SYMBOL, :TRANS_TYPE, :PRICE, :AMOUNT, :BALANCE_CHANGE)",
                   table_name=session["h_table"], DATE_TIME=date_time, NAME=data[i][0], SYMBOL=data[i][1], TRANS_TYPE="Liquidation",
                   PRICE=data[i][2], AMOUNT=data[i][3], BALANCE_CHANGE="+"+data[i][4])

    # clear session variables
    session["data"] = None
    session["new_balance"] = None

    # success
    flash("Stocks sold! New balance: {}".format(session["balance"]))
    return redirect(url_for("portfolio"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Search for stock quote."""
    # POST
    if request.method == "POST":

        # ensure input
        if not request.form.get("symbol"):
            flash("Please enter a stock symbol.")
            return redirect(url_for("quote"))

        # get info
        info = lookup(request.form.get("symbol"))

        # check for correct formatting
        if info == 1:
            flash("Please exclude commas (,) and carots (^) in stock symbols.")
            return (url_for("quote"))

        # ensure both stock and stock price exist
        if info == 2:
            flash("Something went wrong during the search...")
            return redirect(url_for("quote"))
        if info == 3:
            flash("Could not find stock price. Sorry!")
            return redirect(url_for("quote"))

        # format price
        info[1] = usd(info[1])

        # remember most recent stock search results
        session["stock_info"] = info

        return render_template("quote.html", info=info, balance=session["balance"])

    # GET
    else:
        return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    # POST
    if request.method == "POST":
        # variables from recent stock quote search
        info = session["stock_info"]

        # ensure input is formatted corectly
        amount = request.form.get("amount")
        if amount.strip("-").replace(".","").isnumeric() is False:
            flash("Please enter a number.")
            return render_template("quote.html", info=info, balance=session["balance"])
        try:
            amount = int(amount)
        except ValueError:
            flash("Please enter a whole number.")
            return render_template("quote.html", info=info, balance=session["balance"])
        if amount < 0:
            flash("Please enter a positive number.")
            return render_template("quote.html", info=info, balance=session["balance"])

        # calculate user's balance after transaction
        cost = float(amount) * float(info[1].strip("$").replace(",",""))
        new_balance = float(session["balance"].strip("$").replace(",", "")) - cost

        # check for sufficient funds
        if new_balance < 0:
            flash(Markup("Insufficient funds! <a href='/add_money'>Add money to your account?</a>"))
            return render_template("quote.html", info=info, balance=session["balance"])

        # remember purchase details
        session["purchase_details"] = (amount, cost, new_balance)

        # continue to transaction confirmation page
        return render_template("buy.html", info=info, balance=session["balance"], new_balance=usd(new_balance), cost=usd(cost))

    # GET
    else:
        return render_template("quote.html", info=session["stock_info"], balance=session["balance"])

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    # POST
    if request.method == "POST":

        # get input from posted form
        rows=db.execute("SELECT * FROM :table_name", table_name=session["p_table"])
        inputs = []
        for row in rows:
            for key,value in row.items():
                if key == "symbol":
                    inp = request.form.get(value)
                    inputs.append([value,inp])

        # ensure any input was posted
        for i in range(0, len(inputs)):
            if inputs[i][1] != "":
                break
            if i == len(inputs) - 1:
                flash("Please ensure amounts were entered.")
                return redirect(url_for("portfolio"))

        # ensure input was entered correctly
        for i in range(0, len(inputs)):
            if inputs[i][1] != "":
                try:
                    inputs[i][1] = int(inputs[i][1])
                except ValueError:
                    flash("Please ensure whole numbers were enetered.")
                    return redirect(url_for("portfolio"))
                if inputs[i][1] < 0:
                    flash("Please ensure positive numbers were entered.")
                    return redirect(url_for("portfolio"))

        # remove any empty input
        def remove():
            while True:
                for i in range(0, len(inputs)):
                    if inputs[i][1] == "":
                        inputs.pop(i)
                        break
                    if i == len(inputs) - 1:
                        return
        remove()

        # ensure user has enough shares to sell desired amount
        for symbol, amount in inputs:
            for row in rows:
                for key,value in row.items():
                    if symbol == value:
                        if row["amount"] < int(amount):
                            flash("You do not own enough shares of {}".format(row["name"]))
                            return redirect(url_for("portfolio"))

        # format data to send to sell.html
        data = []       # [stock name, stock symbol, current price per share, amount to sell, monetary gain]
        for i in range(0, len(inputs)):
            info = lookup(inputs[i][0])
            dat = []
            dat.append(info[0])                                 # name (string)
            dat.append(inputs[i][0])                            # symbol (string)
            dat.append(usd(info[1]))                            # price (usd(float))
            dat.append(inputs[i][1])                            # amount (int)
            dat.append(usd(info[1] * float(inputs[i][1])))      # gain (usd(float))
            data.append(dat)

        # calculate new balance after transaction
        total_gain = float(0)
        for i in range(0, len(data)):
            total_gain += float(data[i][4].strip("$").replace(",",""))
        new_balance = float(session["balance"].strip("$").replace(",","")) + total_gain

        # remember variables
        session["data"] = data
        session["new_balance"] = new_balance    # float

        return render_template("sell.html", data=data, total_gain=usd(total_gain), new_balance=usd(new_balance))

    # GET
    return redirect(url_for("portfolio"))

@app.route("/add_money", methods=["GET", "POST"])
@login_required
def add_money():
    """Add money to current user's account."""
    # get current user's balance
    balance = float(session["balance"].strip("$").replace(",", ""))

    # POST
    if request.method == "POST":

        # ensure depoit amount is formatted correctly
        deposit = request.form.get("amount").strip("$").replace(",","")
        try:
            deposit = float(deposit)
        except ValueError:
            flash("Please enter an amount.")
            return render_template("add_money.html")
        if deposit < 0:
            flash("Please enter an amount greater than zero!")
            return render_template("add_money.html")

        # update user's balance and session["balance"]
        db.execute("UPDATE users SET balance=:value WHERE id=:ID", value=usd(balance+deposit), ID=session["user_id"])
        session["balance"] = usd(balance + deposit)
        return redirect(url_for("profile"))

    # GET
    return render_template("add_money.html", balance=usd(balance))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Display profile services."""
    return render_template("profile.html", balance=(session["balance"]))

@app.route("/unregister", methods=["GET", "POST"])
@login_required
def unregister():
    """Unregister current user"""
    # POST
    if request.method == "POST":
        # delete user from database, delete user portfolio/history, and forget session variables
        db.execute("DROP TABLE :table", table=session["user"]+"_portfolio")
        db.execute("DROP TABLE :table", table=session["user"]+"_history")
        db.execute("DELETE FROM 'users' WHERE id=:ID", ID=session["user_id"])
        session.clear()

        flash("Account deleted!")
        return redirect(url_for("login"))

    # GET
    return render_template("unregister.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # POST
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide a username!")
            return redirect(url_for("login"))

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide a password!")
            return redirect(url_for("login"))

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE user=:user", user=request.form.get("username"))

        # check for at least one registered user
        if len(rows) < 1:
            flash("Invalid username and/or password.")
            return redirect(url_for("login"))

        # hash password provided
        hashed = hashlib.sha512(request.form.get("password").encode("UTF-8")).hexdigest()

        # ensure username/password is correct
        if request.form.get("username") != rows[0]["user"] or hashed != rows[0]["pw"]:
            flash("Invalid username and/or password.")
            return redirect(url_for("login"))

        # remember user information
        session["user_id"] = rows[0]["id"]
        session["balance"] = rows[0]["balance"]
        session["user"] = rows[0]["user"]
        session["p_table"] = session["user"] + "_portfolio"
        session["h_table"] = session["user"] + "_history"

        # redirect user to home page
        flash('You were successfully logged in!')
        return redirect(url_for("index"))

    # GET
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    # forget session variables
    session.clear()

    # redirect user to login form
    flash('You were successfully logged out!')
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # POST
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide a username!")
            return redirect(url_for("register"))

        # ensure username isn't taken
        rows = db.execute("SELECT * FROM users WHERE user=:username", username=request.form.get("username"))
        if len(rows) == 1:
            flash("Username already taken!")
            return redirect(url_for("register"))

        # ensure both passwords were submitted and match
        if not request.form.get("password1"):
            flash("Must provide a password!")
            return redirect(url_for("register"))
        if not request.form.get("password2"):
            flash("Must provide matching passwords!")
            return redirect(url_for("register"))
        if request.form.get("password1") != request.form.get("password2"):
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        # enter new user into database with hashed password
        hashed = hashlib.sha512(request.form.get("password1").encode("UTF-8")).hexdigest()
        db.execute("INSERT INTO users (user, pw, balance) VALUES(:user, :pw, :balance)", user=request.form.get("username"),
                                                                                         pw=hashed, balance=usd(0))
        # remember user's ID, username, and balance
        rows = db.execute("SELECT * FROM users WHERE user = :user", user=request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        session["user"] = rows[0]["user"]
        session["balance"] = rows[0]["balance"]

        # create and remember portfolio table for new user
        session["p_table"] = session["user"] + "_portfolio"
        db.execute("CREATE TABLE :table_name ('name' TEXT, 'symbol' TEXT, 'amount' INTEGER)", table_name=session["p_table"])

        # create and remember history table for new user
        session["h_table"] = session["user"] + "_history"
        db.execute("CREATE TABLE :table_name ('date_time' TEXT, 'name' TEXT, 'symbol' TEXT, 'trans_type' TEXT,"
                  "'price' TEXT, 'amount' INTEGER, 'balance_change' TEXT)", table_name=session["h_table"])

        # redirect user to home page
        flash('Account successfuly registered!')
        return redirect(url_for("index"))

    # GET
    return render_template("register.html")
