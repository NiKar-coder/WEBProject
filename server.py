from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return render_template('index.html', result="dd")
    else:
        return render_template('index.html', result="")


if __name__ == '__main__':
    app.run(host='192.168.1.2', port='8080', debug=True)
