import os

from request_api.fixer_io_request_api import FixerIoRequestApi
from request_api.mock_request_api import MockRequestApi


def get_request_api():
	if os.getenv("API_ENV") == "FIXER":
		return FixerIoRequestApi()
	else:
		return MockRequestApi()
