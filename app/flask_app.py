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
	return str(request_api.get_latest_rate())


@app.route('/history')
def history():
	return str(request_api.get_history_rate(
		start_date=request.args.get("start"),
		end_date=request.args.get("end"),
	))