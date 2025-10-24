from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('resume.html', title='Резюме')

@main.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти')
