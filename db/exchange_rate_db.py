class ExchangeRateDb:

	def __init__(self, db_client):
		self.db_client = db_client

	def _db_connect(self):
		return self.db_client.get_conn_engine().connect()

	def latest_rate_to_db(self, json_result):
		conn = self._db_connect()

		try:
			sql = "DELETE FROM {schema}.{tablename} {sqlfilter}".format(
				schema=self.schema,
				tablename=self.table_name,
				sqlfilter=self.get_exists_filter()
			)




			conn.execution_options(autocommit=True).execute(sql)
		finally:
			if not conn.closed:
				conn.close()
