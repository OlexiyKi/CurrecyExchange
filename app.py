from flask import Flask, request, render_template
import sqlite3
from database_funcsion import DBManager
from celery_working import add
import al_db
import models_db
from sqlalchemy import select
from sqlalchemy.orm import Session
import os
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':

        return 'Ok'
    else:
        pass
    return '<p>login!</p>'


@app.route('/logout', methods=['GET'])
def logout_user():
    add.apply_async(args= (1, 2))
    return '<p>logout!</p>'


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    return '<p>registration form</p>'


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

        cur_exchange_buy = round(buy_rate_2 / buy_rate_1, 2)
        cur_exchange_sale = round(sale_rate_2 / sale_rate_1, 2)

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
        return render_template('data_form.html')



@app.route('/user_page', methods=['GET'])
def user_access():
    return 'more function'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)




