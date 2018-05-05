from flask import Flask, request
from domain.exchange_rate_api import ExchangeRateApi

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
