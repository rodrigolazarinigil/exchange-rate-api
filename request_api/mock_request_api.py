import requests
import requests_mock
import re


class MockRequestApi:
	def __init__(self):
		self.adapter = requests_mock.Adapter()
		self.session = requests.Session()
		self.session.mount('http://data.fixer.io', self.adapter)
		self.adapter.register_uri(
			method="GET", url='http://data.fixer.io/request_api/latest',
			text='{"rates": {"USD": 1.201633}, "base": "EUR", "date": "2018-05-01", "success": "True", "timestamp": 1525183803}'
		)
		matcher = re.compile('http://data.fixer.io/request_api/([\d]{4}-[\d]{2}-[\d]{2})')
		self.adapter.register_uri(
			method="GET", url=matcher,
			text="""
				{"success": "True", "rates": {"USD": 1.201496}, "timestamp": 1514851199, "base": "EUR","date": "2018-01-01",
				"historical": "True"}
			"""
		)
	
	def get_latest_rate(self):
		r = self.session.get(
			url="http://data.fixer.io/request_api/latest?access_key=c73bd725bbdbb2aac42fff231c619&base=EUR&symbols=USD")
		return str(r.json())
	
	def get_historical_rate_by_range(self):
		r = self.session.get(
			url="http://data.fixer.io/request_api/2018-01-01?access_key=c73bd725bbdbac4a292fff231c619&base=EUR&symbols=USD")
		return str(r.json())


if __name__ == "__main__":
	print(MockRequestApi().get_latest_rate())
