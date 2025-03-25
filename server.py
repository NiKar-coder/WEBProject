from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.owners import Owner

db_session.global_init("db/CarNumbers.db")
app = Flask(__name__)


def redirect_():
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    rendered_template = render_template('index.html', result="")
    if request.method == 'POST':
        try:
            db_sess = db_session.create_session()
            input_ = request.form['input_']
            for owner in db_sess.query(Owner).filter(Owner.carsNumber
                                                     == input_):
                res = f"ФИО: {owner.surname} {owner.name} {owner.patronymic}, квартира: {owner.flat}, телефон: {owner.phone}, модель машины: {owner.carsModel}"
            db_sess.close()
            return render_template('index.html', result=res)
        except Exception:
            return rendered_template
    else:
        return rendered_template


@app.route('/add', methods=['GET', 'POST'])
def add():
    rendered_template = render_template('addPage.html')
    if request.method == 'POST':
        try:
            owner = Owner()
            owner.carsNumber = request.form['numberInput']
            owner.surname = request.form['surnameInput']
            owner.name = request.form['nameInput']
            owner.patronymic = request.form['patronymicInput']
            owner.flat = request.form['flatInput']
            owner.phone = request.form['phoneInput']
            owner.carsModel = request.form['carInput']
            db_sess = db_session.create_session()
            db_sess.add(owner)
            db_sess.commit()
            db_sess.close()
            return redirect_()
        except Exception:
            return rendered_template
    else:
        return rendered_template


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    rendered_template = render_template('removePage.html')
    if request.method == 'POST':
        try:
            db_sess = db_session.create_session()
            input_ = request.form['input_']
            db_sess.query(Owner).filter(Owner.carsNumber == input_).delete()
            db_sess.commit()
            db_sess.close()
            return redirect_()
        except Exception:
            return rendered_template
    else:
        return rendered_template


if __name__ == '__main__':
    app.run(host='192.168.1.2', port='8080', debug=True)
