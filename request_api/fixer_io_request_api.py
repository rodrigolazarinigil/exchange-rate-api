import requests


class FixerIoRequestApi:
	def __init__(self):
		self.latest_rate_url = \
			"http://data.fixer.io/request_api/latest?access_key=c73bd725bbdbb2aac4a292fff231c619&base=EUR&symbols=USD"
		self.historical_rate_by_range_url = \
			"http://data.fixer.io/request_api/2018-01-01?access_key=c73bd725bbdbb2aac4a292fff231c619&base=EUR&symbols=USD"

	def get_latest_rate(self):
		r = requests.get(url=self.latest_rate_url)
		return str(r.json())

	def get_historical_rate_by_range(self):
		r = requests.get(url=self.historical_rate_by_range_url)
		return str(r.json())
