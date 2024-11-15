import time
import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from tkinter.font import names

from flask import Flask, render_template, request, redirect, url_for, abort
from flask.json import dumps
from time import time
app = Flask(__name__) #main



@app.get("/")
def home_world():
    return render_template('index.2.html')


@app.get('/menu')
def menu():
    pizzas = [
        {"name": "Маргарита", "ingredients": "риба, сир с плесеню", "price": 1500},
        {"name": "Пепероні", "ingredients": "тісто, тісто, пепероні", "price": 18},
        {"name": "Гавайська", "ingredients": " соус, моцарела, шинка, ананас", "price": 0}
    ]
    order = request.args.get('order', 'asc')
    return render_template('index.html', order=order, pizzas=pizzas)
@app.get("/home/")
def hello_world():
    return render_template("index3.html", title="ПіццаУпаняно")



@app.get("/login/")
def get_login():
    return render_template("login.html")


@app.post("/login/")
def post_login():
    user = request.form["name"]
    info = request.user_agent
    if user == "aboba":
        abort(401)
    if user == "admin":
        return f"Are you is {user}from {info}"
    else:
        return redirect(url_for("get_login"), code=302)


@app.get("/info/")
def info():
    return (f"URL:\n{url_for("index")}\n"
            f"{url_for("choice")}\n"
            f"{url_for("get_login")}\n"
            f"{url_for("info")}\n")

@app.errorhandler(404)
def page_not_found(error):
    return ""





max_score = 100
test_name = "Python Challenge"
students = [
  {"name": "Vlad", "score": 100},
  {"name": "Sviatoslav", "score": 99},
  {"name": "Юстин", "score": 100},
  {"name": "Viktor", "score": 79},
  {"name": "Ярослав", "score": 93},
]

@app.get('/results')
def results():
  context={
     "title": "Results",
     "students": students,
     "test_name": test_name,
     "max_score": max_score,

  }
  return render_template("results2.html", **context)



@app.get("/add/")
def index():
    create_table()
    return render_template("index.html")

def create_table():
    connect = sqlite3.connect("database.db")
    connect.execute("""
        CREATE TABLE IF NOT EXISTS PARTICIPANTS  (name TEXT, ingredients TEXT, price TEXT)
    """)


@app.get("/join/")
def get_join():
    return render_template("join.html")


@app.post("/join/")
def post_join():
    name = request.form["name"]
    price = request.form["price"]
    ingridients = request.form["ingridients"]
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()

        try:
            cursor.execute("""
                     CREATE TABLE IF NOT EXISTS PARTICIPANTS (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT,
                         ingredients TEXT,
                         price REAL
                     )
                     """)
        except sqlite3.Error as e:
            print("Помилка", e)

        data = (name, price, ingridients)
        try:
            cursor.execute("""
                    INSERT INTO PARTICIPANTS (name, ingredients, price)
                    VALUES (?, ?, ?)""", data)
            users.commit()
            pizza_id = cursor.lastrowid  # подивився документацію це потрібно для того щоб отримувати айди конкретної піцци
        except sqlite3.Error as e:
            print("Помилка", e)
            return "Виникла помилка", 500

    return redirect(url_for("pizza_details", pizza_id=pizza_id))


@app.get("/find_pizza/<int:pizza_id>")
def pizza_details(pizza_id):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()

        try:
            cursor.execute("""
            SELECT name, price, ingredients FROM PARTICIPANTS WHERE id = ?
            """, (pizza_id,))
            pizza = cursor.fetchone()  # теж подивився в документації. це щоб отримати результат
        except sqlite3.Error as e:
            print("Помилка при зчитуванні даних:", e)
            return "Виникла помилка при зчитуванні даних з бази.", 500

    if pizza:
        return render_template("participants.html", data=[pizza])
    else:
        return "Піцу не знайдено", 404

@app.get("/participants")
def get_participants():
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM PARTICIPANTS")
            participants = cursor.fetchall()
        except sqlite3.Error as e:
            print("Помилка", e)
            return "Виникла", 500

    return render_template("participants.html", data=participants)






if __name__ == "__main__":
    app.run(port=8010, debug=True)
