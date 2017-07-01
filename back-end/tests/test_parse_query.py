"""
This is the test suite for methods related to parsing search queries for the
Yummly API.
"""
import unittest
from unittest import mock
from api_functions import parse_search_results

""" Method to create mock data for parsing tests."""
def mocked_response_query(keyword):
	class MockResponse:
		def __init__(self, json_data, status_code):
			self.json = json_data
			self.status_code = status_code

		def json(self):
			return self.json

	if keyword == 'server error':
		return MockResponse(None, 500)
	elif keyword == 'rate limit':
		return MockResponse(None, 409)
	elif keyword == 'bad request':
		return MockResponse(None, 400)

def mocked_response():
	class MockResponse:
		def __init__(self, json_data, status_code):
			self.json = json_data
			self.status_code = status_code

		def json(self):
			return self.json

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

	return MockResponse(mock_json_data, 200)


"""
Test methods related to parsing error results of search queries in Yummly API
"""
class TestParseErrorResults(unittest.TestCase):

	# Test returning an error message for 500 response
	def test_parse_server_error_response(self):
		server_error_mock = mocked_response_query('server error')
		self.assertEqual('server error', parse_search_results(server_error_mock))

	# Test returning an error message for 409 response
	def test_parse_rate_limit_response(self):
		rate_limit_mock = mocked_response_query('rate limit')
		self.assertEqual('rate limit exceeded', parse_search_results(rate_limit_mock))

	# Test returning an error message for 400 response
	def test_parse_bad_request_response(self):
		bad_request_mock = mocked_response_query('bad request')
		self.assertEqual('bad request', parse_search_results(bad_request_mock))


"""
Test method related to parsing successful results of search queries in Yummly
API
"""
class TestParseSuccessResults(unittest.TestCase):

	# Test returning a recipe match for 200 response
	request_mock = mocked_response()
	@mock.patch.object('api_functions.requests.Response', 'json', return_value=request_mock.json())
	def test_parse_success_response(self):
		expected_recipe_id = 'Easy-French-Onion-Soup-2038937'
		self.assertEqual(expected_recipe_id, parse_search_results(request_mock))


if __name__ == '__main__':
	unittest.main()