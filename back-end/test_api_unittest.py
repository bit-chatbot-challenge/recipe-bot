import unittest
from recipe_bot import get_search_results

"""
This is the test suite for methods related to querying the Yummly API.
"""
class TestAPI(unittest.TestCase):
	# Test making search via API
	def test_search_api(self):
		
		#search with malformed request
		expected_bad_result = 400
		bad_search_term = ""
		bad_response = get_search_results(bad_search_term)
		self.assertEqual(expected_bad_result, bad_response.status_code)

		# #simple search for onion soup
		# expected_simple_result = "ok"
		# simple_search_term = "onion soup"
		# self.assert_equal()

		
		# Test simple search with good data
		# Test search with allergy parameter


	# Test parsing search results and returning highest rated query

if __name__ == '__main__':
	unittest.main()