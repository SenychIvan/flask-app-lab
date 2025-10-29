from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

# -------- Контактна форма --------
class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(message="Поле обов'язкове!")])
    email = StringField("Email", validators=[DataRequired(), Email(message="Некоректний email!")])
    message = TextAreaField("Повідомлення", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Надіслати")

# -------- Форма входу --------
class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача / Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")
