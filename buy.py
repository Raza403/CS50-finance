@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        #take symbol from user
        symbl = request.form.get("symbol")
        if not symbl:
            return apology ("Must enter the symbol")
        #Number of shares to buy    
        num = request.form.get("number")
        number = float (num)
        if number is None or number == '' or number < 1:
            return apology ("Please enter valid number of stocks to buy")
       
           
        #Lookup and save dict in quoted    
        quoted = lookup(symbl)
        #If symbol is invalid return apology
        if not quoted:
            return apology ("Invalid stock")
        else:
            #qtd saves price of share
            qtd = quoted["price"]
            #price of single share * Number of sahres required to buy
            prc = float(qtd) * number
            #remember session id
            ide = session["user_id"]
           
            csh = db.execute("SELECT * FROM users WHERE id = :ide", ide = ide)
            #Only go forward if user have enough money
            if prc <= csh[0]["cash"]:
                symb = db.execute ("select * from portfolio where id = :ii" , ii = ide)
                #If it is first trade of user
                if not symb:
                    db.execute("INSERT INTO portfolio (id, symbol,price,shares) VALUES (:ide, :symbol, :price, :shares)", ide = ide,symbol = symbl, price = prc, shares = number)
                    db.execute("UPDATE users SET cash = :cash WHERE id = :ide",cash = csh[0]["cash"] - prc, ide = ide)
                #If user has already bought some shares
                else:        
                    #If user is buying that share again then just update portfolio
                    if symb[0]["symbol"] == symbl :
                        num =int (symb[0]["shares"]) + number
                        db.execute("update portfolio set price = :price, shares = :shares  where id = :ide AND symbol = :smb", price = symb[0]["price"] + prc, ide = ide, shares = num,smb = symbl)
                        db.execute("UPDATE users SET cash = :cash WHERE id = :ide",cash = csh[0]["cash"] - prc, ide = ide)
                        return redirect(url_for("index"))
                    else:
                        #If user is buying that specific share first time then add it to portfolio
                        db.execute("INSERT INTO portfolio (id, symbol,price,shares) VALUES (:ide, :symbol, :price,:shares)", ide = ide,symbol = symbl, price = prc, shares = number)
                        db.execute("UPDATE users SET cash = :cash WHERE id = :ide",cash = csh[0]["cash"] - prc, ide = ide)
                        #Go to index page
                        return redirect(url_for("index"))
            else:
                return apology ("You don't have enough cash to buy these stocks")
    else:
        return render_template("buy.html")
