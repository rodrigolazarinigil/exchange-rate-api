from flask import Flask, request

from util.api_functions import get_requester

app = Flask(__name__)
request_api = get_requester()


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
