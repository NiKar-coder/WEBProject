from flask import Flask, render_template, request
from data import db_session
from data.owners import Owner

db_session.global_init("db/CarNumbers.db")
# owner = Owner()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'searchBtn' in request.form:
            try:
                db_sess = db_session.create_session()
                input_ = request.form['input_']
                for owner in db_sess.query(Owner).filter(Owner.carsNumber
                                                         == input_):
                    res = f"ФИО: {owner.surname} {owner.name} {owner.patronymic}, квартира: {owner.flat}, телефон: {owner.phone}, модель машины: {owner.carsModel}"
                db_sess.close()
                return render_template('index.html', result=res)
            except Exception:
                return render_template('index.html', result="")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        return render_template('addPage.html')
    else:
        return render_template('addPage.html')


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        return render_template('removePage.html')
    else:
        return render_template('removePage.html')


if __name__ == '__main__':
    app.run(host='192.168.1.2', port='8080', debug=True)
