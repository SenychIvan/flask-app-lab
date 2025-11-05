from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import ContactForm
import logging

# створюємо blueprint для головних сторінок
main = Blueprint('main', __name__)

# ✅ Додай цей маршрут для головної сторінки
@main.route('/')
def home():
    return render_template('resume.html')  # або 'contacts.html', якщо немає resume.html


@main.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # ✅ логування у файл з правильним кодуванням UTF-8
        logging.basicConfig(
            filename="contact_log.txt",
            level=logging.INFO,
            encoding="utf-8",
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        logging.info(f"{name} ({email}): {message}")

        flash(f"Дякуємо, {name}! Ваше повідомлення успішно надіслано.", "success")
        return redirect(url_for("main.contacts"))

    return render_template("contacts.html", title="Контакти", form=form)
