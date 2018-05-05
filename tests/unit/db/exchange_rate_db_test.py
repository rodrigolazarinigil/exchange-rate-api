from unittest import TestCase, mock

from db.exchange_rate_db import ExchangeRateDb
from util.db_connection import PostgresClient
import os


class ExchangeRateDbTest(TestCase):
	
	def setUp(self):
		os.environ["USER"] = 'exchange_rate_user'
		os.environ["PWD"] = 'password'
		os.environ["HOST"] = 'localhost'
		os.environ["PORT"] = '5432'
		os.environ["DB"] = 'exchange_rate'
		self.object = ExchangeRateDb(PostgresClient())
	
	# @mock.patch("{}.ExchangeRateDb.db_connect".format(ExchangeRateDb.__module__))
	def latest_rate_to_db_test(self):
		input_json = {
			'rates': {'USD': 1.201633}, 'base': 'EUR', 'date': '2018-05-01', 'success': True,
			'timestamp': 1525183803
		}
		self.object.latest_rate_to_db(input_json)
		# mock_db_connect.assert_called_with()