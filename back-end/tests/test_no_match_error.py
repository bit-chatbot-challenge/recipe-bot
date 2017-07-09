"""
This is the test suite for the custom NoMatchError class
"""
import unittest
from no_match_error import NoMatchError

"""
Test methods related to creating and using NoMatchError
"""
class TestNoMatchError(unittest.TestCase):

	# Test trying to create a NoMatchError with insufficient parameters
	def test_fail_to_create_error(self):
		self.assertRaises(TypeError, NoMatchError)

	# Test creating a NoMatchError
	def test_create_error(self):
		assert NoMatchError('onion soup')
		assert NoMatchError('onion soup', allergy='thyme')

	# Test that appropriate messages are generated based on parameters
	def test_error_messages(self):
		criteria = str({'allergy': 'thyme'})
		self.assertEqual('No matching recipes found for onion soup', 
						 NoMatchError('onion soup').message())
		self.assertEqual('No matching recipes found for onion soup with the following search criteria: ' + criteria,
						 NoMatchError('onion soup', allergy="thyme").message())

if __name__ == '__main__':
	unittest.main()