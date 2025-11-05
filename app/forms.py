from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

# -------- Контактна форма --------
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Поле обов'язкове!")])
    email = StringField("Email", validators=[DataRequired(), Email(message="Некоректний email!")])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=5, max=20, message="Некоректний номер телефону!")])
    subject = StringField("Subject", validators=[DataRequired(), Length(max=100, message="Занадто довга тема!")])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=5, message="Повідомлення має бути довшим!")])
    submit = SubmitField("Send")

# -------- Форма входу --------
class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача / Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")
