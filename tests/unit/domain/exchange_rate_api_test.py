from unittest import TestCase, mock

from domain.exchange_rate_api import ExchangeRateApi
import os
import datetime


class ExchangeRateApiTest(TestCase):
	
	def setUp(self):
		os.environ["USER"] = 'exchange_rate_user'
		os.environ["PWD"] = 'password'
		os.environ["HOST"] = 'localhost'
		os.environ["PORT"] = '5432'
		os.environ["DB"] = 'exchange_rate'
		os.environ["API_ENV"] = ""
		self.object = ExchangeRateApi()
	
	@mock.patch("{}.ExchangeRateDb".format(ExchangeRateApi.__module__))
	def get_db_test(self, mock_exchange_db):
		"""
			Checks if db object is created only once
		"""
		self.object.get_db()
		self.object.get_db()
		
		mock_exchange_db.assert_called_once_with(db_client=mock.ANY)
	
	@mock.patch("{}.FixerIoRequester".format(ExchangeRateApi.__module__))
	@mock.patch("{}.MockRequester".format(ExchangeRateApi.__module__))
	def get_requester_test(self, mock_mock_requester, mock_fixer_requester):
		"""
			Ensure that db object is created only once
		"""
		requester = self.object.get_requester()
		self.assertEqual(mock_mock_requester(), requester)
		
		os.environ["API_ENV"] = "FIXER"
		requester = self.object.get_requester(force_update=True)
		self.assertEqual(mock_fixer_requester(), requester)
	
	@mock.patch("{}.MockRequester".format(ExchangeRateApi.__module__))
	@mock.patch("{}.ExchangeRateDb".format(ExchangeRateApi.__module__))
	def save_latest_rate_test(self, mock_exchange_rate_db, mock_mock_requester):
		"""
			Checks if the return from the requester is sent to the correct db method
		"""
		mock_mock_requester().get_latest_rate.return_value = "LATESTRATE"
		
		self.object.save_latest_rate()
		mock_mock_requester().get_latest_rate.assert_called_with()
		mock_exchange_rate_db().save_json_rate_to_db.assert_called_with('LATESTRATE')
	
	@mock.patch("{}.ExchangeRateDb".format(ExchangeRateApi.__module__))
	def get_latest_rate_test(self, mock_exchange_rate_db):
		"""
			Checks if the value returned is the same returned from the db
		:return:
		"""
		mock_exchange_rate_db().get_latest.return_value = {
			'date': datetime.datetime(2020, 9, 25, 23, 0), 'usd_value': 1.99013608}
		
		latest_rate = self.object.get_latest_rate()
		self.assertEqual({
			'date': datetime.datetime(2020, 9, 25, 23, 0), 'usd_value': 1.99013608}, latest_rate)
	
	@mock.patch("{}.ExchangeRateDb".format(ExchangeRateApi.__module__))
	def get_history_rate_test(self, mock_exchange_rate_db):
		result = self.object.get_history_rate('2018-05-01', '2018-05-05')
		mock_exchange_rate_db().get_history.assert_called_with('2018-05-01', '2018-05-05')
		self.assertEqual(mock_exchange_rate_db().get_history.return_value, result)
