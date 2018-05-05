from pandas._libs.lib import timedelta

from domain.exchange_rate_db import ExchangeRateDb
from request.fixer_io_requester import FixerIoRequester
from request.mock_requester import MockRequester
import os

from util.db_connection import PostgresClient


class ExchangeRateApi:
	
	def __init__(self):
		self.requester = self.get_requester()
		self.db = ExchangeRateDb(db_client=PostgresClient())
	
	@staticmethod
	def get_requester():
		if os.getenv("API_ENV") == "FIXER":
			return FixerIoRequester()
		else:
			return MockRequester()
	
	def save_latest_rate(self):
		rate = self.requester.get_latest_rate()
		print(rate)
		self.db.save_json_rate_to_db(rate)
	
	def get_latest_rate(self):
		return self.db.get_latest()
	
	# def get_historical_rate_by_range(self, start_date, end_date):
	# 	for n in range(int((end_date - start_date).days)):
	# 		rate = self.requester.get_historical_rate_by_range(start_date + timedelta(n))
	# 		self.db.save_json_rate_to_db(rate)
	#
	# 	return None
