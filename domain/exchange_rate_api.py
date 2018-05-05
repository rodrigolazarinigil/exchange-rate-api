from domain.exchange_rate_db import ExchangeRateDb
from request.fixer_io_requester import FixerIoRequester
from request.mock_requester import MockRequester
import os


class ExchangeRateApi:
	
	def __init__(self):
		self.requester = self.get_requester()
		self.db = ExchangeRateDb()
	
	@staticmethod
	def get_requester():
		if os.getenv("API_ENV") == "FIXER":
			return FixerIoRequester()
		else:
			return MockRequester()
	
	def get_latest_rate(self):
		rate = self.requester.get_latest_rate()
		self.db.save_record(rate)
		
		return rate
		
	
	def get_historical_rate_by_range(self, start_date, end_date):
		return self.requester.get_historical_rate_by_range(date)
	
		self.db.save_record(rate)