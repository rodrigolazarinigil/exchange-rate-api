import os
import sqlalchemy


class PostgresClient:
	"""
		Postgres client connection
	"""
	conn_engine = None
	
	@classmethod
	def get_conn_engine(cls) -> sqlalchemy.engine.Engine:
		"""
			Returns a connection engine. Created only once for instance.
		"""
		if cls.conn_engine is None:
			connection_string = "postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}".format(
				user=os.getenv("POSTGRES_USER"),
				pwd=os.getenv("POSTGRES_PASSWORD"),
				host=os.getenv("HOST"),
				port=os.getenv("PORT"),
				db=os.getenv("POSTGRES_DB")
			)
			
			cls.conn_engine = sqlalchemy.create_engine(
				connection_string,
				pool_size=5,
				max_overflow=0
			)
		
		return cls.conn_engine
