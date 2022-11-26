from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        pass
    else:
        pass
    return '<p>login!</p>'


@app.route('/logout', methods=['GET'])
def logout_user():
    return '<p>logout!</p>'


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    return '<p>registration form</p>'


@app.route('/user_page', methods=['GET'])
def user_access():
    return 'more function'


@app.route('/currency', methods=['GET', 'POST'])
def currency_converter():
    return 'currency_converter'

