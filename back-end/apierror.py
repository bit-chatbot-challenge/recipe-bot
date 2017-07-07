"""
Custom exception for errors related to pinging the Yummly API
"""
class APIError(Exception):
	def __init__(self, status_code):
		self.status_code = status_code
		self.message_mapping = { 500: 'Yummly cannot complete request due to internal server error',
								 409: 'Our bot has exceeded the number of API calls in our plan',
								 400: 'We are submitting a bad request to the API' }

	def message(self):
		if self.status_code not in self.message_mapping:
			return 'Unknown error'
		else:
			return self.message_mapping[self.status_code]