from decimal import Decimal
from unittest import TestCase, mock

from domain.exchange_rate_db import ExchangeRateDb
from util.db_connection import PostgresClient
import os
import datetime


class ExchangeRateDbTest(TestCase):
	
	def setUp(self):
		os.environ["USER"] = 'exchange_rate_user'
		os.environ["PWD"] = 'password'
		os.environ["HOST"] = 'localhost'
		os.environ["PORT"] = '5432'
		os.environ["DB"] = 'exchange_rate'
		self.object = ExchangeRateDb(PostgresClient())
	
	@mock.patch("{}.ExchangeRateDb.db_connect".format(ExchangeRateDb.__module__))
	@mock.patch("{}.sqlalchemy".format(ExchangeRateDb.__module__))
	@mock.patch("{}.insert".format(ExchangeRateDb.__module__))
	def save_record_test(self, mock_insert, mock_sqlalchemy, mock_db_connect):
		mock_sqlalchemy.MetaData.return_value = 'METADATA'
		mock_table = mock_sqlalchemy.Table
		mock_sqlalchemy.Date.return_value = 'DATETYPE'
		mock_sqlalchemy.TIMESTAMP.return_value = 'TIMESTAMPTYPE'
		mock_sqlalchemy.Float.return_value = 'FLOATTYPE'
		mock_sqlalchemy.Column.side_effect = lambda name, coltype: name + '---' + coltype()
		mock_insert_stmt = mock_insert().values().on_conflict_do_nothing
		
		input_value = {
			'date': '2017-01-01', 'timestamp': 1514851199, 'usd_value': 1.3
		}
		
		self.object.save_record(input_value)
		mock_table.assert_called_with(
			'euro_to_dollar_rate', 'METADATA', 'date---DATETYPE', 'timestamp---TIMESTAMPTYPE',
			'usd_value---FLOATTYPE', schema='exchange')
		mock_insert_stmt.assert_called_with(index_elements=['date', 'timestamp'])
		mock_db_connect.assert_called_with()
	
	@mock.patch("{}.ExchangeRateDb.save_record".format(ExchangeRateDb.__module__))
	def latest_rate_to_db_test(self, mock_save_record):
		input_json = {
			'rates': {'USD': 1.201633}, 'base': 'EUR', 'date': '2018-05-01', 'success': True,
			'timestamp': 1525183803
		}
		
		self.object.save_json_rate_to_db(input_json)
		mock_save_record.assert_called_with(
			values_dict={
				'date': '2018-05-01', 'timestamp': datetime.datetime(2018, 5, 1, 11, 10, 3),
				'usd_value': 1.201633})
	
	@mock.patch("{}.ExchangeRateDb.save_record".format(ExchangeRateDb.__module__))
	def historical_rate_to_db_test(self, mock_save_record):
		input_json = {
			'success': True, 'rates': {'USD': 1.201496}, 'timestamp': 1514851199, 'base': 'EUR',
			'date': '2018-01-01', 'historical': True}
		self.object.save_json_rate_to_db(input_json)
		mock_save_record.assert_called_with(
			values_dict={
				'usd_value': 1.201496, 'timestamp': datetime.datetime(2018, 1, 1, 21, 59, 59),
				'date': '2018-01-01'})
	
	@mock.patch("{}.ExchangeRateDb.db_connect".format(ExchangeRateDb.__module__))
	@mock.patch("{}.sqlalchemy".format(ExchangeRateDb.__module__))
	def get_history_test(self, mock_sql_alchemy, mock_db_connect):
		mock_sql_alchemy.text.return_value = 'QUERYTEXT'
		mock_db_connect().execute().fetchall.return_value = [
			(datetime.date(2018, 5, 1), datetime.datetime(2018, 5, 1, 23, 0), Decimal('19.37371628')),
			(datetime.date(2018, 5, 2), datetime.datetime(2018, 5, 2, 23, 0), Decimal('87.74356140'))
		]
		
		result = self.object.get_history('2018-05-01', '2018-05-05')
		mock_sql_alchemy.text.assert_called_with(mock.ANY)
		mock_db_connect().execute.assert_called_with('QUERYTEXT', end_date='2018-05-05', start_date='2018-05-01')
		
		expected_result = [
			{
				'date': datetime.date(2018, 5, 1),
				'timestamp': datetime.datetime(2018, 5, 1, 23, 0),
				'usd_value': 19.37371628
			},
			{
				'date': datetime.date(2018, 5, 2),
				'timestamp': datetime.datetime(2018, 5, 2, 23, 0),
				'usd_value': 87.7435614
			}
		]
		
		self.assertEqual(expected_result, result)