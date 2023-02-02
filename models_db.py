from sqlalchemy import Column, Integer, String, Float
from al_db import Base

class Currency(Base):
    __tablename__ = 'my_currency'
    id = Column(Integer, primary_key=True, unique=True)
    bank = Column(String(50))
    currency = Column(String(120))
    date_exchange = Column(String(120))
    buy_rate = Column(Float)
    sale_rate = Column(Float)

    def __init__(self, bank, currency, date_exchange, buy_rate, sale_rate):
        self.bank = bank
        self.currency = currency
        self.date_exchange = date_exchange
        self.buy_rate = buy_rate
        self.sale_rate = sale_rate

    def __repr__(self):
        return f'<Currency {self.name!r}>'



class User(Base):
       __tablename__ = 'users'
       id = Column(Integer, primary_key=True, unique=True)
       username = Column(String(50))
       password = Column(String(50))
       email = Column(String(50))

       def __int__(self, username, password, email):
           self.username = username
           self.password = password
           self.email = email

       def __repr__(self):
           return f'<User {self.username!r}>'
