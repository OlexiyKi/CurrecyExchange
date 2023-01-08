from flask import Flask, request, render_template
import sqlite3
from database_funcsion import DBManager
from celery_working import add
import al_db
import models_db
from sqlalchemy import select

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        conn = al_db.engine.connect()
        res1 = select([models_db.User])
        result = conn.execute(res1)
        data_res = result.fetchall()
        print(result)
        pass
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

        with DBManager() as db:
            buy_rate_1, sale_rate_1 = db.get_result(f'SELECT buy_rate, sale_rate FROM currency WHERE bank="{user_bank}" AND date_exchange="{user_date}" AND currency="{user_currency_1}"')
            buy_rate_2, sale_rate_2 = db.get_result(f'SELECT buy_rate, sale_rate FROM currency WHERE bank="{user_bank}" AND date_exchange="{user_date}" AND currency="{user_currency_2}"')

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




