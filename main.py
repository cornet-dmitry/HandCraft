from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config
# from PIL import Image

from images import convert_to_binary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# user = SQLAlchemy(app)


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


# class User(user.Model):
#     id = user.Column(user.Integer, primary_key=True)


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
        # img = request.form['img']

        print(title, price)

        item = Item(title=title, price=price)

        try:
            item.session.add(item)
            item.session.commit()
            return redirect('/')
        except Exception as ex:
            return 'Ошибка добавления товара: ' + str(ex)
    return render_template("create.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/sing-in')
def sing_in():
    return render_template("sing-in.html")


if __name__ == '__main__':
    app.run(debug=True)
