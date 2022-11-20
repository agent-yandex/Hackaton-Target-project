from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(10)])
    submit = SubmitField('Продолжить')


class EnterForm(FlaskForm):
    phone = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Продолжить')