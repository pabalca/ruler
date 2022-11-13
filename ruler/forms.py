from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

from ruler.models import Symbol


class RuleForm(FlaskForm):
    ticker = SelectField("Ticker", validators=[DataRequired()])
    action = SelectField("Action", validators=[DataRequired()], choices=[("more_than","more than"), ("less_than","less than"), ("alert", "alert")])
    price = FloatField("Price", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AutoTraderForm(FlaskForm):
    name = StringField("Autotrader", validators=[DataRequired()])
    submit = SubmitField("Create")


class SymbolForm(FlaskForm):
    name = StringField("Symbol", validators=[DataRequired()])
    submit = SubmitField("Create")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")


