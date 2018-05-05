import requests


class FixerIoRequester:
	def __init__(self):
		self.latest_rate_url = \
			"http://data.fixer.io/request_api/latest?access_key=c73bd725bbdbb2aac4a292fff231c619&base=EUR&symbols=USD"
		self.historical_rate_by_range_url = \
			"http://data.fixer.io/request_api/{date}?access_key=c73bd725bbdbb2aac4a292fff231c619&base=EUR&symbols=USD"

	def get_latest_rate(self):
		r = requests.get(url=self.latest_rate_url)
		return r.json()

	def get_historical_rate_by_range(self, date):
		r = requests.get(url=self.historical_rate_by_range_url.format(date=date))
		return r.json()
