from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.owners import Owner
import json

db_session.global_init("db/CarNumbers.db")
app = Flask(__name__)


def redirect_():
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            db_sess = db_session.create_session()
            input_ = request.form['input_']
            for owner in db_sess.query(Owner).filter(Owner.carsNumber
                                                     == input_):
                name = owner.name
                surname = owner.surname
                patronymic = owner.patronymic
                flat = owner.flat
                phone = owner.phone
                carsModel = owner.carsModel
            db_sess.close()
            with open('excluded.json', 'r') as file:
                excluded = json.load(file)
            print(excluded)
            for el in excluded['excluded']:
                for _ in el:
                    if el == input_:
                        return render_template('index.html', alert="true",
                                               message="Номер внесен в ЧС")
            return render_template('index.html', res="true", result="ФИО: " +
                                   surname + " "
                                   + name + " " +
                                   patronymic + ", квартира: " + flat +
                                   ", номер телефона: " + phone +
                                   ", модель автомобиля: " +
                                   carsModel)
        except Exception:
            return render_template('index.html', res="false", alert="false")
    else:
        return render_template('index.html', res="false", alert="false")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            owner = Owner()
            carsNumber = request.form['numberInput']
            surname = request.form['surnameInput']
            name = request.form['nameInput']
            patronymic = request.form['patronymicInput']
            flat = request.form['flatInput']
            phone = request.form['phoneInput']
            carsModel = request.form['carInput']
            owner.carsNumber = carsNumber
            owner.surname = surname
            owner.name = name
            owner.patronymic = patronymic
            owner.flat = flat
            owner.phone = phone
            owner.carsModel = carsModel
            db_sess = db_session.create_session()
            db_sess.add(owner)
            db_sess.commit()
            db_sess.close()
            return render_template('addPage.html',
                                   alert="true",
                                   message="Номер " + carsNumber
                                   +
                                   " успешно добавлен")
        except Exception:
            return render_template('addPage.html', alert="true",
                                   message="Ошибка добавления")
    else:
        return render_template('addPage.html', alert="false")


@app.route('/DB_login', methods=['GET', 'POST'])
def DB_login():
    if request.method == 'POST':
        try:
            login = request.form['loginInput']
            password = request.form['passwordInput']
            with open('admins.json', 'r') as file:
                admins = json.load(file)
            for el in admins['admins']:
                if login == el['login'] and password == el['password']\
                        and el['db'] == "true":
                    return render_template('login.html', alert="true",
                                           login="true",
                                           message="Вы успешно вошли"
                                           )
            return render_template('login.html', alert="true",
                                   message="Неверный логин или пароль",
                                   login="false")
        except Exception:
            return render_template('login.html', alert="true",
                                   message="Ошибка входа",
                                   login="false")
    else:
        return render_template('login.html', alert="false",
                               login="false")


@app.route('/editDB')
def editDB():
    return render_template('editDB.html')


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        try:
            db_sess = db_session.create_session()
            input_ = request.form['input_']
            db_sess.query(Owner).filter(Owner.carsNumber == input_).delete()
            db_sess.commit()
            db_sess.close()
            return render_template('removePage.html', alert="true",
                                   message=f"Номер {input_} успешно удален")
        except Exception:
            return render_template('removePage.html', alert="true",
                                   message="Ошибка удаления")
    else:
        return render_template('removePage.html', alert="false")


if __name__ == '__main__':
    app.run(host='192.168.1.2', port='8080', debug=True)
