import urllib

import config

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_required, logout_user, LoginManager, UserMixin, login_manager
from forms.user import RegisterForm, LoginForm

from changeImage import resize

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY
db = SQLAlchemy(app)

ACTIVE_ID = 0


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String)
    text = db.Column(db.Text)
    category = db.Column(db.String)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'({self.id}, {self.login}, {self.mail}, {self.password}, {self.isAdmin})'

    def check_password(self, password):
        pass


db.create_all()


@app.route('/')
def index():
    items = Item.query.all()
    return render_template("index.html", data=items)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        print(request.form)
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']

        try:
            img = open(f'static/images/{str(request.form["image"])}', "w")
            resize(img, img)
        except Exception as ex:
            return render_template('error.html', message=['Ошибка загрузки фотографии', str(ex), config.ERROR_TEMPLATE])

        print(f'({title}, {price}, {img}, {text})')
        item = Item(title=title, price=price, image=img, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return render_template('error.html', message=['Ошибка добавления товара', str(ex), config.ERROR_TEMPLATE])
    return render_template("create.html")


@app.route('/login', methods=["POST", "GET"])
def login():

    form = LoginForm()
    if form.submit.data:
        users = db.session.query_property(Users).all()
        count = 0
        for user in users:
            if user.mail == form.mail.data:

                if user.mail == form.mail.data and user.password == form.password.data:

                    if user.isAdmin is False:
                        return render_template('index_logged.html')
                    elif user.isAdmin is True:
                        return render_template('index_dev_logged.html')
                else:
                    return render_template('login.html',
                                           message="Неправильный логин или пароль",
                                           form=form)
            else:
                count += 1
                if count == len(users):
                    return render_template('login.html',
                                           message="Неправильный логин или пароль",
                                           form=form)
                continue
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.submit.data:
        users = db.session.query(Users).all()

        if form.password.data == '' or form.password_again.data == '':
            return render_template('register.html', form=form,
                                   message='Введите пароль')

        if '@' not in form.mail.data and '.' not in form.mail.data:
            return render_template('register.html', form=form,
                                   message='Неверный формат почты. Отсутствует "@" и "."')

        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form,
                                   message="Пароли не совпадают")

        for user in users:
            if user.mail == form.mail.data:
                return render_template('register.html', form=form,
                                       message="Такой пользователь уже есть")

        try:
            user = Users(
                login=form.login.data,
                mail=form.mail.data,
                password=form.password.data,
                isAdmin=True
            )
            db.session.add(user)
            db.session.commit()
            flash("Вы успешно зарегистрировались!")
            return render_template('index_logged.html')
        except Exception as ex:
            return render_template('error.html', message=['Ошибка создания аккаута', str(ex), config.ERROR_TEMPLATE])
    return render_template('register.html', form=form)


@app.route('/index_logged')
def index_logged():
    items = Item.query.all()
    return render_template("index_logged.html", data=items)


@app.route('/index_dev_logged')
def index_dev_logged():
    items = Item.query.all()
    return render_template("index_dev_logged.html", data=items)


@app.route('/about_logged')
def about_logged():
    return render_template("about_logged.html")


@app.route('/about_dev_logged')
def about_dev_logged():
    return render_template("about_dev_logged.html")


@app.route('/logout/')
def logout():
    return redirect('/')


@app.route('/error')
def error(message):
    return render_template('/error', message=message)


if __name__ == '__main__':
    app.run(debug=True)
