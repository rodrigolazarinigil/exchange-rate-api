from domain.exchange_rate_db import ExchangeRateDb
from request.fixer_io_requester import FixerIoRequester
from request.mock_requester import MockRequester
import os

from util.db_connection import PostgresClient


class ExchangeRateApi:
	
	def __init__(self):
		self._requester = None
		self._db = None
		
	def get_db(self):
		if self._db is None:
			self._db = ExchangeRateDb(db_client=PostgresClient())
		
		return self._db
	
	def get_requester(self, force_update=False):
		if self._requester is None or force_update:
			if os.getenv("API_ENV") == "FIXER":
				self._requester = FixerIoRequester()
			else:
				self._requester = MockRequester()
		
		return self._requester
	
	def save_latest_rate(self):
		rate = self.get_requester().get_latest_rate()
		self.get_db().save_json_rate_to_db(rate)
	
	def get_latest_rate(self):
		return self.get_db().get_latest()
	
	def get_history_rate(self, start_date, end_date):
		return self.get_db().get_history(start_date, end_date)
