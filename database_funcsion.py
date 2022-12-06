import sqlite3, datetime


class DBManager:
    def __enter__(self):
        self.con = sqlite3.connect('currency')
        self.cur = self.con.cursor()
        return self

    def get_result(self, query):
        res = self.cur.execute(query)
        data = res.fetchone()
        return data

    def write_data(self, query):
        self.cur.execute(query)
        self.con.commit()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()


def generate_data():
    data = [
        {'bank': 'A1', 'currency': 'UAH', 'buy_rate': 1.05, 'sale_rate': 0.95},
        {'bank': 'A1', 'currency': 'USD', 'buy_rate': 1, 'sale_rate': 1},
        {'bank': 'A1', 'currency': 'UAH', 'buy_rate': 1.05, 'sale_rate': 0.95},
        {'bank': 'A1', 'currency': 'UAH', 'buy_rate': 1.05, 'sale_rate': 0.95}
        ]

    with DBManager() as db:
        for line in data:
            bank = line['bank']
            currency = line['currency']
            buy_rate = line['buy_rate']
            sale_rate = line['sale_rate']

            date_exchange = datetime.datetime.now().strftime('%Y-%m-%d')
            query = f'INSERT INTO currency (bank, currency, date_exchange, buy_rate, sale_rate) VALUES ("{bank}", "{currency}", "{date_exchange}", {buy_rate}, {sale_rate})'
            db.write_data(query)


generate_data()