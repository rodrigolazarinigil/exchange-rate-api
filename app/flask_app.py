from flask import Flask, request
from domain.exchange_rate_api import ExchangeRateApi
import os

os.environ["USER"] = 'exchange_rate_user'
os.environ["PWD"] = 'password'
os.environ["HOST"] = 'localhost'
os.environ["PORT"] = '5432'
os.environ["DB"] = 'exchange_rate'

app = Flask(__name__)
request_api = ExchangeRateApi()


@app.route('/latest')
def latest():
	return request_api.get_latest_rate()


@app.route('/history')
def history():
	return request_api.get_historical_rate_by_range(
		start_date=request.args.get("start"),
		end_date=request.args.get("end"),
	)

# {'rates': {'USD': 1.201633}, 'base': 'EUR', 'date': '2018-05-01', 'success': True, 'timestamp': 1525183803}

# {'success': True, 'rates': {'USD': 1.201496}, 'timestamp': 1514851199, 'base': 'EUR', 'date': '2018-01-01', 'historical': True}
