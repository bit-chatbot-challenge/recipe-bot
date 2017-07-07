"""
This is the test suite for methods related to parsing search queries for the
Yummly API.
"""
import unittest
from unittest.mock import Mock
from api_functions import parse_response
from request_error import RequestError

"""
Test methods related to parsing error results of search queries in Yummly API
"""
class TestParseErrorResults(unittest.TestCase):

	def setUp(self):
		self.keyword = 'search'

	# Test returning an error message for 500 response
	def test_parse_server_error_response(self):
		mock_response = Mock(status_code=500)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning an error message for 409 response
	def test_parse_rate_limit_response(self):
		mock_response = Mock(status_code=409)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning an error message for 400 response
	def test_parse_bad_request_response(self):
		mock_response = Mock(status_code=400)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)


"""
Test method related to parsing successful results of search queries in Yummly
API
"""
class TestParseSuccessResults(unittest.TestCase):

	# Test parsing a recipe match for 200 response
	def test_parse_success_response(self):
		keyword = 'search'
		mock_json_data = { 'criteria': { 'excludedIngredient': None, 
										 'q': 'onion soup', 
										 'allowedIngredient': None
									   }, 
						   'totalMatchCount': 89479, 
						   'matches': [{ 'recipeName': 'Easy French Onion Soup',
										 'id': 'Easy-French-Onion-Soup-2038937', 
										 'flavors': None, 
										 'ingredients': ['butter', 
														 'onions', 
														 'au jus gravy mix', 
														 'water'], 
										 'rating': 3,
										 'attributes': {'course': ['Soups']}, 
										 'totalTimeInSeconds': 2100, 
										 'sourceDisplayName': 'McCormick', 
										 'smallImageUrls': ['https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s90'],
										 'imageUrlsBySize': {'90': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s90-c'}
									   }],
						   'attribution': { 'html': "Recipe search powered by <a href='http://www.yummly.co/recipes'><img alt='Yummly' src='https://static.yummly.co/api-logo.png'/></a>",
											'logo': 'https://static.yummly.co/api-logo.png',
											'url': 'http://www.yummly.co/recipes/',
											'text': 'Recipe search powered by Yummly'
										  }, 
						   'facetCounts': {}}

		mock_response = Mock(status_code=200)
		mock_response.json.return_value = mock_json_data
		expected_recipe_id = 'Easy-French-Onion-Soup-2038937'
		self.assertEqual(expected_recipe_id, parse_response(keyword, mock_response))


if __name__ == '__main__':
	unittest.main()