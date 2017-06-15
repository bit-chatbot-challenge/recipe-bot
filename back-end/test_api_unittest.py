import unittest
from recipe_bot import get_search_results

"""
This is the test suite for methods related to querying the Yummly API.
"""
class TestAPI(unittest.TestCase):

	# simple search for onion soup
	def test_simple_search_api(self):
		expected_simple_result = 200
		simple_search_term = "onion soup"
		simple_response = get_search_results(simple_search_term)
		self.assertEqual(expected_simple_result, simple_response.status_code)

		# Test search with allergy parameter


	# Test parsing search results and returning highest rated query

if __name__ == '__main__':
	unittest.main()