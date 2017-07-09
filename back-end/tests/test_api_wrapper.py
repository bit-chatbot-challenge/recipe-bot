"""
This is the test suite for the wrapper for methods related to the Yummly API.
"""
import unittest
from api_functions import get_recipe_info

"""
Test the wrapper method for retreiving info from the API
"""
class TestAPIWrapper(unittest.TestCase):

	def setUp(self):
		self.search_term = 'onion soup'

	# Test the wrapper method for a simple search: one search term, no options,
	# no scaling
	def test_api_wrapper_simple(self):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '3.0 tbsps butter',
									  				 	 '3.0 medium onions, thinly sliced',
									  				 	 '1.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '3.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 4
		recipe_info = get_recipe_info(self.search_term, desired_servings)
		self.assertEqual(expected_recipe_info, recipe_info)

if __name__ == '__main__':
	unittest.main()