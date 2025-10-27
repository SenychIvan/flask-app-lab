from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response

users_bp = Blueprint('users', __name__, template_folder='templates')


# ---------------------- старі маршрути ----------------------
@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get("age", 0)
    return render_template("users/hi.html", name=name.upper(), age=age)

@users_bp.route('/admin')
def admin():
    return redirect(url_for("users.greetings", name="Administrator", age=45))


# ---------------------- нові маршрути (лаб 4) ----------------------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # прості тестові дані
        if username == 'ivan' and password == '12345':
            session['user'] = username
            flash('Вхід успішний!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Невірні дані для входу!', 'danger')
            return redirect(url_for('users.login'))

    return render_template('users/login.html')


@users_bp.route('/profile')
def profile():
    if 'user' not in session:
        flash('Спочатку увійдіть у систему!', 'warning')
        return redirect(url_for('users.login'))

    username = session['user']
    cookies = request.cookies
    theme = request.cookies.get('theme', 'light')  # 🟢 додаємо зчитування теми
    return render_template('users/profile.html', username=username, cookies=cookies, theme=theme)


@users_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Ви вийшли із системи!', 'info')
    return redirect(url_for('users.login'))


# ---------------------- cookies ----------------------
@users_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'user' not in session:
        flash('Спочатку увійдіть у систему!', 'warning')
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    value = request.form.get('value')
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie(key, value)
    flash(f'Кукі \"{key}\" додано!', 'success')
    return resp


@users_bp.route('/delete_cookie/<key>')
def delete_cookie(key):
    resp = make_response(redirect(url_for('users.profile')))
    resp.delete_cookie(key)
    flash(f'Кукі \"{key}\" видалено!', 'info')
    return resp


# ---------------------- зміна теми ----------------------
@users_bp.route('/theme/<mode>')
def theme(mode):
    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('theme', mode)
    flash(f'Тема змінена на {mode}!', 'info')
    return resp
