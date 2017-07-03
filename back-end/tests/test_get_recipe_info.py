"""
This is the test suite for methods related to getting recipes from the Yummly
API and returning URLs and scaled ingredient list
"""

import unittest
from api_functions import create_url_for_user

"""
Test methods related to creating URL to return to user
"""
class TestCreatingUrl(unittest.TestCase):

	# Test creating a URL to view a recipe given a recipe id
	def test_create_url(self):
		recipe_id = 'Easy-French-Onion-Soup-2038937'
		expected_url = 'http://www.yummly.com/recipe/' + recipe_id
		self.assertEqual(expected_url, create_url_for_user(recipe_id))

if __name__ == '__main__':
	unittest.main()