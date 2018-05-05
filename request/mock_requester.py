import requests
import requests_mock
import re
import random


class MockRequester:
	def __init__(self):
		self.history_re_pattern = "(http://data.fixer.io/request_api/)([\d]{4}-[\d]{2}-[\d]{2})"
		self.adapter = requests_mock.Adapter()
		self.session = requests.Session()
		self.session.mount('http://data.fixer.io', self.adapter)
		self.adapter.register_uri(
			method="GET", url='http://data.fixer.io/request_api/latest',
			text='{"rates": {"USD": 1.201633}, "base": "EUR", "date": "2018-05-01", "success": "True", "timestamp": 1525183803}'
		)
		matcher = re.compile('http://data.fixer.io/request_api/([\d]{4}-[\d]{2}-[\d]{2})')
		# noinspection PyTypeChecker
		self.adapter.register_uri(
			method="GET", url=matcher,
			text=self._history_callback
		)
	
	def get_latest_rate(self):
		r = self.session.get(
			url="http://data.fixer.io/request_api/latest?access_key=c73bd725bbdbb2aac42fff231c619&base=EUR&symbols=USD")
		return r.json()
	
	def get_historical_rate_by_range(self, date, end_date):
		r = self.session.get(
			url="""
				http://data.fixer.io/request_api/{date}?access_key=c73bd725bbdbac4a292fff231c619&base=EUR&symbols=USD
			""".format(
				date=date
			)
		)
		
		return r.json()
	
	def _history_callback(self, request, context):
		m = re.search(pattern=self.history_re_pattern, string=request.url)
		if m:
			date = m.group(2)
		
		return """
			{{"success": "True", "rates": {{"USD": {fakerate}}}, "timestamp": 1514851199, "base": "EUR","date": "{date}",
			"historical": "True"}}
		""".format(date=date, fakerate=random.uniform(1, 2))