from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.owners import Owner
import json
import os

db_session.global_init("db/CarNumbers.db")
app = Flask(__name__)

admins = {
    "admins": [
        {
            "login": "admin",
            "password": "admin",
            "db": "true",
            "excluded": "true",
            "admins": "true"
        }
    ]
}
if not os.path.exists('admins.json'):
    with open('admins.json', 'w+') as admins_file:
        json.dump(admins, admins_file, ensure_ascii=False)
excluded = {
    "excluded": ["о000оо"]
}
if not os.path.exists('excluded.json'):
    with open('excluded.json', 'w+') as excluded_file:
        json.dump(excluded, excluded_file, ensure_ascii=False)


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


@app.route('/editAdmins_login', methods=['GET', 'POST'])
def editAdmins_login():
    if request.method == 'POST':
        try:
            login = request.form['loginInput']
            password = request.form['passwordInput']
            with open('admins.json', 'r') as file:
                admins = json.load(file)
            for el in admins['admins']:
                if login == el['login'] and password == el['password']\
                        and el['admins'] == "true":
                    return render_template('editAdmins_login.html',
                                           alert="true",
                                           login="true",
                                           message=f"Здравствуйте, {login}"
                                           )
            return render_template('editAdmins_login.html', alert="true",
                                   message="У Вас нет прав администратора " +
                                   "или введены неверные данные",
                                   login="false")
        except Exception:
            return render_template('editAdmins_login.html', alert="true",
                                   message="Ошибка входа",
                                   login="false")
    else:
        return render_template('editAdmins_login.html', alert="false",
                               login="false")


@app.route('/editAdmins')
def editAdmins():
    return render_template('editAdmins.html')


@app.route('/addAdmin', methods=['GET', 'POST'])
def addAdmin():
    if request.method == 'POST':
        try:
            login = request.form['loginInput']
            password = request.form['passwordInput']
            try:
                request.form['DB_access']
                DB_access = "true"
            except Exception:
                DB_access = "false"
            try:
                request.form['BL_access']
                BL_access = "true"
            except Exception:
                BL_access = "false"
            try:
                request.form['admins_access']
                admins_access = "true"
            except Exception:
                admins_access = "false"
            with open('admins.json', 'r') as file:
                admins = json.load(file)
                admins['admins'].append({
                    "login": login,
                    "password": password,
                    "db": DB_access,
                    "excluded": BL_access,
                    "admins": admins_access
                })
            with open('admins.json', 'w') as file:
                json.dump(admins, file, ensure_ascii=False)
            return render_template('addAdmin.html', alert="true",
                                   message=f"Админ {login} успешно добавлен")
        except Exception:
            return render_template('addAdmin.html', alert="true",
                                   message="Ошибка добавления")
    else:
        return render_template('addAdmin.html', alert="false")


@app.route('/removeAdmin', methods=['GET', 'POST'])
def removeAdmin():
    if request.method == 'POST':
        try:
            input_ = request.form['input_']
            with open('admins.json', 'r') as file:
                admins = json.load(file)

            list_ = admins['admins']
            for el in list_:
                if el['login'] == input_:
                    list_.remove(el)
            with open('admins.json', 'w') as file:
                json.dump(admins, file, ensure_ascii=False)
            return render_template('removeAdmin.html', alert="true",
                                   message=f"Админ {input_} успешно удален")
        except Exception:
            return render_template('removeAdmin.html', alert="true",
                                   message="Ошибка удаления")
    else:
        return render_template('removeAdmin.html', alert="false")


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
                    return render_template('DB_login.html', alert="true",
                                           login="true",
                                           message=f"Здравствуйте, {login}"
                                           )
            return render_template('DB_login.html', alert="true",
                                   message="У Вас нет прав администратора " +
                                   "или введены неверные данные",
                                   login="false")
        except Exception:
            return render_template('DB_login.html', alert="true",
                                   message="Ошибка входа",
                                   login="false")
    else:
        return render_template('DB_login.html', alert="false",
                               login="false")


@app.route('/editBL_login', methods=['GET', 'POST'])
def editBL_login():
    if request.method == 'POST':
        try:
            login = request.form['loginInput']
            password = request.form['passwordInput']
            with open('admins.json', 'r') as file:
                admins = json.load(file)
            for el in admins['admins']:
                if login == el['login'] and password == el['password']\
                        and el['excluded'] == "true":
                    return render_template('BL_login.html', alert="true",
                                           login="true",
                                           message=f"Здравствуйте, {login}"
                                           )
            return render_template('BL_login.html', alert="true",
                                   message="У Вас нет прав администратора " +
                                   "или введены неверные данные",
                                   login="false")
        except Exception:
            return render_template('BL_login.html', alert="true",
                                   message="Ошибка входа",
                                   login="false")
    else:
        return render_template('BL_login.html', alert="false",
                               login="false")


@app.route('/editBL', methods=['GET', 'POST'])
def editBL():
    return render_template('editBL.html')


@app.route('/addBL', methods=['GET', 'POST'])
def addBL():
    if request.method == 'POST':
        try:
            carsNumber = request.form['input_']
            with open('excluded.json', 'r') as file:
                excluded = json.load(file)
            excluded['excluded'].append(carsNumber)
            with open('excluded.json', 'w') as file:
                json.dump(excluded, file, ensure_ascii=False)
            return render_template('addBL.html', alert="true",
                                   message="Номер " + carsNumber +
                                   " успешно добавлен в ЧС")
        except Exception:
            return render_template('addBL.html', alert="true",
                                   message="Ошибка добавления")
    else:
        return render_template('addBL.html', alert="false")


@app.route('/deleteBL', methods=['GET', 'POST'])
def deleteBL():
    if request.method == 'POST':
        try:
            carsNumber = request.form['input_']
            with open('excluded.json', 'r') as file:
                excluded = json.load(file)
            for el in excluded['excluded']:
                if el == carsNumber:
                    excluded['excluded'].remove(el)
            with open('excluded.json', 'w') as file:
                json.dump(excluded, file, ensure_ascii=False)
            return render_template('removePage.html', alert="true",
                                   message="Номер " +
                                   carsNumber +
                                   " успешно удален из ЧС")
        except Exception:
            return render_template('removePage.html', alert="true",
                                   message="Ошибка удаления")
    else:
        return render_template('removePage.html', alert="false")


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
