import click

from ruler import app
from ruler.models import User, Rule, Symbol, db
from ruler.utils import Alert
import requests


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Rule=Rule, User=User)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")

    u = User(username="admin", pwd="admin")
    db.session.add(u)
    db.session.commit()
    click.echo("Admin user created.")


@app.cli.command()
@click.option("-p", "--pwd", prompt="Rule", help="Create new user.")
def createuser(pwd):
    u = User(pwd)
    db.session.add(u)
    db.session.commit()
    click.echo(f"{u.id} user created.")


@app.cli.command()
def check():
    alert = Alert()
    rules = Rule.query.filter(Rule.active == True).all()
    for rule in rules:
        ticker = rule.ticker
        price = rule.price
        action = rule.action
        print(f"Rule {rule}")

        symbol = Symbol.query.filter(Symbol.name.contains(ticker)).first()
        alert = Alert()
        if action == "more_than" and symbol.price > price:
                r = alert.send_message(f"{ticker} = {symbol.price}, alert more_than {price}")
                rule.active = False
        elif action == "less_than" and symbol.price < price:
                r = alert.send_message(f"{ticker} = {symbol.price}, alert less_than {price}")
                rule.active = False
        elif action == "alert":
                r= alert.send_message(f"Alert {ticker} = $ {symbol.price}")
                rule.active = False
        else:
            click.echo(f"Error: {action} {symbol.price} {price}")

        db.session.commit()



@app.cli.command()
def update():
    delete = Symbol.query.all()
    for d in delete:
        db.session.delete(d)
    r = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50"
    )
    symbols = [
        (token["symbol"], token["current_price"]) for token in r.json()
    ]

    for symbol in symbols:
        s = Symbol(name=symbol[0], price=symbol[1])
        db.session.add(s)
    db.session.commit()
