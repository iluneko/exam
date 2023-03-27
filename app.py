from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import sqlite3
import pandas as pd
import sqlite3

db = sqlite3.connect('lingbattle.db')
cur = db.cursor()

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lingbattle.db'
db = SQLAlchemy()

class User(db.Model): # пол и возраст пользователя (+ студент / не студент).
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    language = db.Column(db.Text)

class Answers(db.Model): # таблица с ответами пользователя на вопросы.
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key = True)
    language = db.Column(db.Text)
    q1 = db.Column(db.Text)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Text)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Text)
    q6 = db.Column(db.Text)
    q7 = db.Column(db.Text)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)

db.init_app(app) # коллабим.

@app.before_first_request # создаём базу данных...
def db_creation():
    db.create_all()

@app.route('/')  
def index():
    return render_template("base.html")

@app.route('/questions') # вопросы с помощью функции, на этой странице опрос.
def questions():
    return render_template(
        'questions.html'
    )

@app.route('/english')
def eng():
    return render_template(
        'english.html'
    )

@app.route('/french')
def fra():
    return render_template(
        'french.html'
    )

@app.route('/spanish')
def esp():
    return render_template(
        'spanish.html'
    )

@app.route('/czech')
def cze():
    return render_template(
        'czech.html'
    )

@app.route('/italian')
def ita():
    return render_template(
        'italian.html'
    )

@app.route('/german')
def german():
    return render_template(
        'german.html'
    )

@app.route('/chinese')
def chn():
    return render_template(
        'chinese.html'
    )

@app.route('/finnish')
def fin():
    return render_template(
        'finnish.html'
    )


@app.route('/process', methods = ['get']) # тут сбор информации...
def answer_process():
    if not request.args:
        return redirect(url_for('questions'))
    
    
    age = request.args.get('age')
    gender = request.args.get('gender')
    education = request.args.get('education')
    language = request.args.get('language')
    
    user = User(
        age = age,
        gender = gender,
        education = education,
        language = language
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    q8 = request.args.get('q8')
    q9 = request.args.get('q9')
    q10 = request.args.get('q10')

    answer = Answers(id = user.id, language = language, q1 = q1, q2 = q2, q3 = q3, q4 = q4, q5 = q5, q6 = q6, q7 = q7, q8 = q8, q9 = q9, q10 = q10)
    db.session.add(answer)
    db.session.commit()
    
    return render_template("answer.html") 

@app.route('/results') # какие результаты + статистика по ответам.
def results():
    all = {}
    ageresults = db.session.query(
    func.avg(User.age),
    func.min(User.age),
    func.max(User.age)
    ).one()
    all['age_mean'] = ageresults[0] # средний возраст респондентов.
    all['age_min'] = ageresults[1] # самый младший респондент.
    all['age_max'] = ageresults[2] # самый старший респондент.
    all['total_count'] = User.query.count() # всего прошло опрос столько...
    all['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0] # средняя оценка схожести грамматики.
    all['q4_mean'] = db.session.query(func.avg(Answers.q4)).one()[0] # средняя оценка сложности алфавита.
    all['q8_mean'] = db.session.query(func.avg(Answers.q8)).one()[0] # средняя оценка сложности грамматики.
    all['q9_mean'] = db.session.query(func.avg(Answers.q9)).one()[0] # как сложно говорить на языке.
    all['q10_mean'] = db.session.query(func.avg(Answers.q10)).one()[0] # средняя оценка красоты звучания языка.
    all['top3_languages'] = db.session.query(Answers.language, (Answers.q2 + Answers.q4 + Answers.q8 + Answers.q9 + Answers.q10)/5).order_by((Answers.q2 + Answers.q4 + Answers.q8 + Answers.q9 + Answers.q10)/5).all()[-3:]

    return render_template('results.html', all = all)

if __name__ == "__main__":
    app.debug = True # чтобы не было багов / устранены недочёты...
    app.run()