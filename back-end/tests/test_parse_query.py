"""
This is the test suite for methods related to parsing search queries for the
Yummly API.
"""
import unittest
from unittest.mock import Mock
from api_functions import parse_search_results

""" Method to create mock data for parsing tests."""
def mocked_response_query():
	class MockResponse:
		def __init__(self, json_data, status_code):
			self.json_data = json_data
			self.status_code = status_code

		def json(self):
			return self.json_data

	return MockResponse(None, 500)


"""
Test methods related to parsing results of search queries in Yummly API
"""
class TestParseResults(unittest.TestCase):

	# Test returning an error message for 500 response
	def test_parse_server_error_response(self):
		server_error_mock = mocked_response_query()
		self.assertEqual('server error', parse_search_results(server_error_mock))


		# server_error_mock = Mock(return_value={ 'criteria': { 'excludedIngredient': None, 
		# 													  'q': 'onion soup', 
		# 													  'allowedIngredient': None
		# 													}, 
		# 										'totalMatchCount': 89479, 
		# 										'matches': [{ 'recipeName': 'Easy French Onion Soup',
		# 													  'id': 'Easy-French-Onion-Soup-2038937', 
		# 													  'flavors': None, 
		# 													  'ingredients': ['butter', 
		# 													  				  'onions', 
		# 													  				  'au jus gravy mix', 
		# 													  				  'water'], 
		# 													  'rating': 3,
		# 													  'attributes': {'course': ['Soups']}, 
		# 													  'totalTimeInSeconds': 2100, 
		# 													  'sourceDisplayName': 'McCormick', 
		# 													  'smallImageUrls': ['https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s90'],
		# 													  'imageUrlsBySize': {'90': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s90-c'}
		# 									   }],
		# 									   'attribution': { 'html': "Recipe search powered by <a href='http://www.yummly.co/recipes'><img alt='Yummly' src='https://static.yummly.co/api-logo.png'/></a>",
		# 									   					'logo': 'https://static.yummly.co/api-logo.png',
		# 									   					'url': 'http://www.yummly.co/recipes/',
		# 									   					'text': 'Recipe search powered by Yummly'
		# 									   				  }, 
		# 									   'facetCounts': {}})

if __name__ == '__main__':
	unittest.main()