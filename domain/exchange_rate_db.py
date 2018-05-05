import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
import datetime


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
	
	def save_json_rate_to_db(self, json_result):
		"""
			Saves data to db based on a JSON
		:param json_result: JSON obtained from the 'latest rate' or 'historical rate' API
			- date and timestamp info must be on the first level;
			- usd_value is inside a rates dictionary
		Example: {
			'rates': {'USD': 1.201633}, 'base': 'EUR', 'date': '2018-05-01', 'success': True,
			'timestamp': 1525183803
		}
		"""
		self.save_record(
			values_dict={
				'date': json_result['date'],
				'timestamp': datetime.datetime.fromtimestamp(json_result['timestamp']),
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
			m = sqlalchemy.MetaData()
			
			rate_table = sqlalchemy.Table(
				"euro_to_dollar_rate", m,
				sqlalchemy.Column('date', sqlalchemy.Date),
				sqlalchemy.Column('timestamp', sqlalchemy.TIMESTAMP),
				sqlalchemy.Column('usd_value', sqlalchemy.Float),
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
	
	def get_latest(self):
		conn = self.db_connect()
		
		try:
			s = sqlalchemy.text("""
				select *
				from exchange.euro_to_dollar_rate
				where (date, "timestamp") = (
					select max(date), max("timestamp") from exchange.euro_to_dollar_rate
				)
			""")
			
			result = conn.execute(s).fetchone()
		
		finally:
			if not conn.closed:
				conn.close()
		
		if result is not None:
			return {
				"date": result["timestamp"],
				"usd_value": float(result["usd_value"])
			}
		else:
			return None
	
	def get_history(self, start_date, end_date):
		conn = self.db_connect()
		
		try:
			s = sqlalchemy.text("""
				select date, "timestamp", usd_value
				from (
					select a.*, row_number() over (partition by date order by "timestamp" desc) as time_order
					from exchange.euro_to_dollar_rate a
					where date between :start_date and :end_date
				) x
				where time_order = 1
			""")
			
			result_query = conn.execute(s, start_date=start_date, end_date=end_date).fetchall()
			result_dict = []
			for x in result_query:
				result_dict.append({
					"date": x[0],
					"timestamp": x[1],
					"usd_value": float(x[2])
				})
		
		finally:
			if not conn.closed:
				conn.close()
		
		return result_dict
