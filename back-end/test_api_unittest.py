import unittest
import os
from recipe_bot import get_search_results, create_payload
from collections import OrderedDict

"""
This is the test suite for methods related to querying the Yummly API.
"""
class TestAPI(unittest.TestCase):

	# Test creating basic request parameters as payload:
	def test_create_basic_payload(self):
		expected_payload = OrderedDict({
			'_app_id': os.environ["AWS_YUMMLY_APP_ID"],
			'_app_key': os.environ['AWS_YUMMLY_APP_KEY'],
			'q': 'onion soup',
		})
		payload = create_payload('onion soup')
		self.assertEqual(expected_payload, payload)

	# Test simple search for onion soup
	def test_simple_search_api(self):
		expected_simple_result = 200
		simple_search_term = "onion soup"
		simple_response = get_search_results(simple_search_term)
		self.assertEqual(expected_simple_result, simple_response.status_code)

	# Test utility for creating payload with optional allergy parameter
	def test_optional_parameter_utility(self):
		expected_payload = OrderedDict({
			'_app_id': os.environ["AWS_YUMMLY_APP_ID"],
			'_app_key': os.environ['AWS_YUMMLY_APP_KEY'],
			'q': 'onion soup',
			'allowedAllergy[]': 'Gluten-Free'
		})

	# Test search with allergy parameter
	def test_allergy_search_api(self):
		expected_allergy_result = 200
		allergy_search_term = "onion soup"
		allergy = "Gluten-Free"
		#allergy_response = get_search_results(allergy_search_term, allergy=allergy)
		#self.assertEqual(expected_allergy_result, allergy_response.status_code)

	# Test search with time parameter
	def test_time_search_api(self):
		expected_time_result = 200
		time_search_term = "onion soup"
		time = "5400"
		# time_response = get_search_results(time_search_term, time=time)
		# self.assertEqual(expected_time_result, time_response.status_code)


	# Test parsing search results and returning highest rated query

if __name__ == '__main__':
	unittest.main()