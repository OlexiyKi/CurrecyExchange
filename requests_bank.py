import requests
import datetime
from sqlalchemy.orm import Session
import al_db, models_db

def get_PrivatBank_data():
    current_date_base = datetime.datetime.now().strftime("%Y-%m-%d")
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")

    r = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={current_date}')
    currency_info = r.json()

    purchaseRate_USD = 0
    saleRate_USD = 0
    for c in currency_info['exchangeRate']:
        if c['currency'] == 'USD':
            purchaseRate_USD = c['purchaseRate']
            saleRate_USD = c['saleRate']

    with Session(al_db.engine) as session:
        record = models_db.Currency(
            bank='PrivatBank',
            currency='UAH',
            date_exchange=current_date_base,
            buy_rate= round(1 / purchaseRate_USD, 3),
            sale_rate= round(1 / saleRate_USD, 3)
        )
        session.add(record)

        for c in currency_info['exchangeRate']:
            if c.get('saleRate') and c.get('currency') != 'USD':
                currency_name = c['currency']
                purchaseRate_currency = round((c['purchaseRate'] / purchaseRate_USD), 2)
                saleRate_currency = round((c['saleRate'] / saleRate_USD), 2)

                record = models_db.Currency(
                    bank='PrivatBank',
                    currency=currency_name,
                    date_exchange=current_date_base,
                    buy_rate=purchaseRate_currency,
                    sale_rate=saleRate_currency
                )
                session.add(record)
                session.commit()


def get_Monobank_data():
    # валюты, которые нас интересуют
    currency_dict = {
        'UAH': 980,
        'USD': 840,
        'EUR': 978,
        'GBP': 826,
        'PLN': 985,
    }
    current_date_base = datetime.datetime.now().strftime("%Y-%m-%d")
    current_date = datetime.datetime.now().timestamp()

    r = requests.get('https://api.monobank.ua/bank/currency')
    currency_info = r.json()

    purchaseRate_USD = 0
    saleRate_USD = 0
    with Session(al_db.engine) as session:
        for cur in currency_info:
            if cur['currencyCodeA'] == currency_dict.get('USD'):
                purchaseRate_USD = cur['rateBuy']
                saleRate_USD = cur['rateSell']
                rec = models_db.Currency(
                    bank = 'MONOBANK',
                    currency = 'UAH',
                    date_exchange = current_date_base,
                    buy_rate = round(1 / purchaseRate_USD, 3),
                    sale_rate = round(1 / saleRate_USD, 3)
                )
                session.add(rec)
                session.commit()
        for currency, iso_currency in currency_dict.items():
            for cur in currency_info:
                if cur['currencyCodeB'] == currency_dict.get('USD'):     #если базовая валюта уже USD, не нужны дополнительные преобразования
                    if iso_currency == cur['currencyCodeA']:
                        purchaseRate_currency = cur['rateBuy']
                        saleRate_currency = cur['rateSell']
                        rec = models_db.Currency(
                            bank='MONOBANK',
                            currency=currency,
                            date_exchange=current_date_base,
                            buy_rate=purchaseRate_currency,
                            sale_rate=saleRate_currency
                        )
                        session.add(rec)
                        session.commit()
                        '''блок ниже для расширения функционала, если у банка расщирится валютный ассортимент и часть его будет привязана только к гривне'''
                # elif cur['currencyCodeB'] == currency_dict.get('UAH'):     #если базовая валюта UAH, делаем дополнительные преобразования
                #     if iso_currency == cur['currencyCodeA']:
                #         purchaseRate_currency = round(cur['rateBuy'] / purchaseRate_USD, 2)
                #         saleRate_currency = round(cur['rateSell'] / saleRate_USD, 2)
                #         rec = models_db.Currency(
                #             bank='MONOBANK',
                #             currency=currency,
                #             date_exchange=current_date_base,
                #             buy_rate=purchaseRate_currency,
                #             sale_rate=saleRate_currency
                #         )
                #         session.add(rec)
                #         session.commit()




#get_PrivatBank_data()
#get_Monobank_data()