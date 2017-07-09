"""
This is the test suite for the custom APIError class
"""
import unittest
from apierror import APIError

"""
Test methods related to creating and using APIError
"""
class TestAPIError(unittest.TestCase):

	# Test trying to create an APIError with insufficient parameters
	def test_fail_to_create_error(self):
		self.assertRaises(TypeError, APIError)

	# Test creating an APIError
	def test_create_error(self):
		assert APIError(500)

	# Test that appropriate messages are generated based on status code
	def test_error_messages(self):
		server_message = 'Yummly cannot complete request due to internal server error'
		limit_message = 'Our bot has exceeded the number of API calls in our plan'
		request_message = 'We are submitting a bad request to the API'
		unknown_message = 'Unknown error'

		self.assertEqual(server_message, APIError(500).message())
		self.assertEqual(limit_message, APIError(409).message())
		self.assertEqual(request_message, APIError(400).message())
		self.assertEqual(unknown_message, APIError(451).message())

if __name__ == '__main__':
	unittest.main()