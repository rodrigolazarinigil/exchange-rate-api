from sqlalchemy import MetaData, Table, Column, Date, Float
from sqlalchemy.dialects.postgresql import *


class ExchangeRateDb:
	"""
		Class responsible for saving new data to the database
	"""
	
	def __init__(self, db_client):
		"""
			Constructor
		:param db_client: A postgres database client with 'get_conn_engine' method
		"""
		self.db_client = db_client
	
	def db_connect(self):
		"""
			Connects to the target db
		:return: DB client connected
		"""
		return self.db_client.get_conn_engine().connect()
	
	def latest_rate_to_db(self, json_result):
		"""
			Saves data to db based on a JSON
		:param json_result: JSON obtained from the 'latest rate' API
		Example: {
			'rates': {'USD': 1.201633}, 'base': 'EUR', 'date': '2018-05-01', 'success': True,
			'timestamp': 1525183803
		}
		"""
		self.save_record(
			values_dict={
				'date': json_result['date'],
				'timestamp': json_result['date'],
				'usd_value': json_result['rates']['USD']
			}
		)
	
	def save_record(self, values_dict):
		"""
			Saves one record, respecting the unique key
		:param values_dict: Dictionary with all the column values from the table
		"""
		conn = self.db_connect()
		
		try:
			m = MetaData()
			
			rate_table = Table(
				"euro_to_dollar_rate", m,
				Column('date', Date),
				Column('timestamp', TIMESTAMP),
				Column('usd_value', Float),
				schema='exchange'
			)
			
			insert_stmt = insert(rate_table).values(**values_dict)
			insert_if_not_exists = insert_stmt.on_conflict_do_nothing(
				index_elements=['date', 'timestamp']
			)
			
			conn.execute(insert_if_not_exists)
		finally:
			if not conn.closed:
				conn.close()
