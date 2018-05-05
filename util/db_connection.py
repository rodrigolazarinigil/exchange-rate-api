import os
import sqlalchemy
from sqlalchemy.dialects.postgresql import insert


class PostgresClient:
	"""
				Classe para encapsular conexão com Postgres
			"""
	conn_engine = None

	@classmethod
	def get_conn_engine(cls) -> sqlalchemy.engine.Engine:
		if cls.conn_engine is None:
			connection_string = "postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}".format(
				user=os.getenv("USER"),
				pwd=os.getenv("PWD"),
				host=os.getenv("HOST"),
				port=os.getenv("PORT"),
				db=os.getenv("DB")
			)

			cls.conn_engine = sqlalchemy.create_engine(
				connection_string,
				pool_size=5,
				max_overflow=0
			)

		return cls.conn_engine

	def save_record(self, insert_stmt, ):
		insert_stmt = insert(table).values(
			id='some_existing_id',
			data='inserted value')

		do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
			index_elements=['id']
		)

		conn.execute(do_nothing_stmt)
