import os

from domain.exchange_rate_api import ExchangeRateApi

os.environ["USER"] = 'exchange_rate_user'
os.environ["PWD"] = 'password'
os.environ["HOST"] = 'localhost'
os.environ["PORT"] = '5432'
os.environ["DB"] = 'exchange_rate'

api = ExchangeRateApi()

api.save_latest_rate()
