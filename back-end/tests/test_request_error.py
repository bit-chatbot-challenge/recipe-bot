"""
This is the test suite for the custom RequestError class
"""
import unittest
from request_error import RequestError

"""
Test methods related to creating and using RequestError
"""
class TestRequestError(unittest.TestCase):

	# Test trying to create a RequestError with insufficient parameters
	def test_fail_to_create_error(self):
		self.assertRaises(TypeError, RequestError)

	# Test creating a RequestError
	def test_create_error(self):
		assert RequestError(500)

	# Test that appropriate messages are generated based on status code
	def test_error_messages(self):
		server_message = 'Yummly cannot complete request due to internal server error'
		limit_message = 'Our bot has exceeded the number of API calls in our plan'
		request_message = 'We are submitting a bad request to the API'
		unknown_message = 'Unknown error'

		self.assertEqual(server_message, RequestError(500).message())
		self.assertEqual(limit_message, RequestError(409).message())
		self.assertEqual(request_message, RequestError(400).message())
		self.assertEqual(unknown_message, RequestError(451).message())

if __name__ == '__main__':
	unittest.main()