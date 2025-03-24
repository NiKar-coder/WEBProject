from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return render_template('index.html', result="Результат поиска: "
                               + "dd")
    else:
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
