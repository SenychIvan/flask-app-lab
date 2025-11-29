from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    session, request, make_response
)
from app.forms import LoginForm
from .. import db
from .models import User
from app.posts.models import Post   # щоб працювали user.posts

# створюємо blueprint
users_bp = Blueprint('users', __name__, template_folder='templates')


# ---------------------------------------------------------
#                   🚀 1. ORM ФУНКЦІОНАЛ (Лаба 8)
# ---------------------------------------------------------

# 🟢 список користувачів
@users_bp.route("/")
def list_users():
    users = User.query.all()
    return render_template("users/list.html", users=users)

# 🟢 додавання користувача
@users_bp.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("Користувача додано!", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/add.html")

# 🟢 пости конкретного користувача
@users_bp.route("/<int:user_id>/posts")
def user_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()
    # або: posts = user.posts
    return render_template("users/user_posts.html", user=user, posts=posts)


# ---------------------------------------------------------
#                   🌐 2. СТАРІ МАРШРУТИ (залишаємо)
# ---------------------------------------------------------

@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get("age", 0)
    return render_template("users/hi.html", name=name.upper(), age=age)


@users_bp.route('/admin')
def admin():
    return redirect(url_for("users.greetings", name="Administrator", age=45))


# ---------------------------------------------------------
#            🔐 3. ЛОГІН (Flask-WTF)
# ---------------------------------------------------------

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        # тестовий логін
        if username == 'ivan' and password == '12345':
            session['user'] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Невірні дані!", "danger")
            return redirect(url_for('users.login'))

    return render_template('users/login.html', form=form)


# ---------------------------------------------------------
#                   👤 4. ПРОФІЛЬ КОРИСТУВАЧА
# ---------------------------------------------------------

@users_bp.route('/profile')
def profile():
    if 'user' not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for('users.login'))

    username = session['user']
    cookies = request.cookies
    theme = request.cookies.get('theme', 'light')

    return render_template("users/profile.html",
                           username=username,
                           cookies=cookies,
                           theme=theme)


@users_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("Ви вийшли із системи!", "info")
    return redirect(url_for('users.login'))


# ---------------------------------------------------------
#                   🍪 5. COOKIE ФУНКЦІЇ
# ---------------------------------------------------------

@users_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'user' not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for('users.login'))

    key = request.form.get("key")
    value = request.form.get("value")

    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie(key, value)

    flash(f'Кукі "{key}" додано!', "success")
    return resp


@users_bp.route('/delete_cookie/<key>')
def delete_cookie(key):
    resp = make_response(redirect(url_for('users.profile')))
    resp.delete_cookie(key)

    flash(f'Кукі "{key}" видалено!', "info")
    return resp


@users_bp.route('/theme/<mode>')
def theme(mode):
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie("theme", mode)

    flash(f"Тема змінена на {mode}!", "info")
    return resp
