from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import or_

from ruler import app
from ruler.models import User, Rule, AutoTrader, Symbol, Tick, db
from ruler.forms import RuleForm, AutoTraderForm, SymbolForm, SearchForm
import json
from ruler.utils import Alert


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    rules = Rule.query.order_by(Rule.created_at.desc())
    if form.validate_on_submit():
        search = form.search.data
        rules = rules.filter(or_(Rule.ticker.contains(search)))
    rules = rules.all()
    return render_template("index.html", form=form, rules=rules)


@app.route("/rule", methods=["GET", "POST"])
def rule():
    form = RuleForm()
    autotraders = AutoTrader.query.all()
    form.ticker.choices = [ (symbol.name, symbol.name) for symbol in Symbol.query.all() ]
    if form.validate_on_submit():
        user = session.get("user")
        # token = session.get("token")
        ticker = form.ticker.data
        action = form.action.data
        price = form.price.data
        # token = form.token.data

        # whitelist = [a.id for a in AutoTrader.query.all()]
        # if token not in whitelist:
        #     flash("Not a valid token")
        #    return render_template("rule.html", form=form)

        r = Rule(ticker=ticker, action=action, price=price)
        db.session.add(r)
        db.session.commit()
        # flash(f"Your rule <{r.id}> is saved.")
        return redirect(url_for("index"))
    return render_template("rule.html", form=form)


@app.route("/clear/<rule_id>", methods=["GET", "POST"])
def clear(rule_id):
    r = Rule.query.get(rule_id)
    db.session.delete(r)
    db.session.commit()
    flash(f"Your rule <{rule_id}> is deleted.")
    return redirect(url_for("index"))


@app.route("/autotrader", methods=["GET", "POST"])
def autotrader():
    form = AutoTraderForm()
    autotraders = AutoTrader.query.order_by(AutoTrader.created_at.desc())
    if form.validate_on_submit():
        name = form.name.data
        a = AutoTrader(name=name)
        db.session.add(a)
        db.session.commit()
        flash(f"Your autotrader <{a.id}> is saved.")
        return redirect(url_for("autotrader"))
    return render_template("autotrader.html", form=form, autotraders=autotraders)


@app.route("/symbol", methods=["GET", "POST"])
def symbol():
    form = SymbolForm()
    symbols = Symbol.query.all()
    return render_template("symbol.html", symbols=symbols)

@app.route("/ticks/<symbol>", methods=["GET"])
def ticks(symbol):
    ticks = Tick.query.order_by(Tick.created_at.desc()).filter(Tick.symbol == symbol).all()
    return render_template("ticks.html", ticks=ticks)
