from flask import Flask, request, render_template
import sqlite3
from database_funcsion import DBManager
import al_db
import models_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask import session as flask_session
#from flask.ext.session import Session as FlaskSession



app = Flask(__name__)
app.secret_key = 'supersecret'


@app.route('/', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        user_username = request.form['username']
        user_psw = request.form['psw']

        with Session(al_db.engine) as session:
            statement = select(models_db.User).filter_by(username=user_username)
            username = session.scalars(statement).first()
            if username is None:
                return render_template('login_form.html',
                                       user_username=user_username,
                                       log_result="go_to_register")
            else:
                if username.password == user_psw:
                    flask_session['username'] = user_username
                    return render_template('login_form.html',
                                           user_username=user_username,
                                           log_result="success",
                                           username=flask_session['username'])

                else:
                    return render_template('login_form.html',
                                           user_username=user_username,
                                           log_result="unsuccess")

    else:
        return render_template('login_form.html')


@app.route('/logout', methods=['GET'])
def logout():
    # remove the username from the session if it's there
    flask_session.pop('username', None)
    return  "<p>logout</p>"



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_username = request.form['username']
        user_email = request.form['email']
        user_psw = request.form['psw']

        with Session(al_db.engine) as session:
            statement = select(models_db.User).filter_by(username = user_username)
            username = session.scalars(statement).first()
            if username is not None:
                if username.username == user_username:
                    return render_template('registration_form.html',
                                       user_username=user_username,
                                       username = username)

            else:
                flag = False
                record = models_db.User(
                    username = user_username,
                    email = user_email,
                    password = user_psw
                )
                session.add(record)
                session.commit()
                return render_template('registration_form.html',
                                       user_username=user_username,
                                       username=username
                                       )

    else:
        return render_template('registration_form.html')



@app.route('/currency', methods=['GET', 'POST'])
def currency_converter():

    if request.method == 'POST':
        user_bank = request.form['bank']  #получаем значения с формы
        user_date = request.form['date']
        user_currency_1 = request.form['currency_1']
        user_currency_2 = request.form['currency_2']

        with Session(al_db.engine) as session:
            statement_1 = select(models_db.Currency).filter_by(bank = user_bank, currency = user_currency_1,
                                                               date_exchange = user_date)
            currency_1 = session.scalars(statement_1).first()
            statement_2 = select(models_db.Currency).filter_by(bank=user_bank, currency=user_currency_2,
                                                               date_exchange=user_date)
            currency_2 = session.scalars(statement_2).first()


        buy_rate_1, sale_rate_1 = currency_1.buy_rate, currency_1.sale_rate

        buy_rate_2, sale_rate_2 = currency_2.buy_rate, currency_2.sale_rate

        cur_exchange_buy = round(buy_rate_2 / buy_rate_1, 3)
        cur_exchange_sale = round(sale_rate_2 / sale_rate_1, 3)

        return render_template('data_form.html',
                               cur_exchange_buy=cur_exchange_buy,
                               cur_exchange_sale=cur_exchange_sale,
                               user_currency_1=user_currency_1,
                               user_currency_2=user_currency_2,
                               user_bank=user_bank,
                               user_date=user_date

                               )
    else:
        """ используем GET чтоб отправить форму в момент перехода по урлу?  """
        if 'username' in flask_session:
            return render_template('data_form.html')
        return 'You have to login for begin'



@app.route('/user_page', methods=['GET'])
def index():
    if 'username' in flask_session:
        return f'Logged in as {flask_session["username"]}'
    return 'You are not logged in'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)




