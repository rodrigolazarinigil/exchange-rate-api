import os
from unittest import TestCase, mock

from util.db_connection import PostgresClient


class PostgresClientTest(TestCase):
	
	def setUp(self):
		os.environ["POSTGRES_USER"] = "testuser"
		os.environ["POSTGRES_PASSWORD"] = "testpwd"
		os.environ["HOST"] = "testhost"
		os.environ["PORT"] = "testport"
		os.environ["POSTGRES_DB"] = "testdb"
		self.object = PostgresClient()
	
	@mock.patch("{}.sqlalchemy".format(PostgresClient.__module__))
	def get_conn_engine_test(self, mock_sql_alchemy):
		mock_sql_alchemy.create_engine.return_value = 'CONNENGINE'
		
		conn_engine = self.object.get_conn_engine()
		
		self.assertEqual('CONNENGINE', conn_engine)
		mock_sql_alchemy.create_engine.assert_called_with(
			'postgresql+psycopg2://testuser:testpwd@testhost:testport/testdb',
			max_overflow=0, pool_size=5)
