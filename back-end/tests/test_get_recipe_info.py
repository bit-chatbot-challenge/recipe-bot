"""
This is the test suite for methods related to getting recipes from the Yummly
API and returning URLs and scaled ingredient list
"""

import unittest
from api_functions import create_url_for_user, get_ingredients_and_servings
from api_functions import get_recipe

"""
Test method related to creating URL to return to user
"""
class TestCreatingUrl(unittest.TestCase):

	# Test creating a URL to view a recipe given a recipe id
	def test_create_url(self):
		recipe_id = 'Easy-French-Onion-Soup-2038937'
		expected_url = 'http://www.yummly.com/recipe/' + recipe_id
		self.assertEqual(expected_url, create_url_for_user(recipe_id))

"""
Test methods related to getting recipe details
"""
class TestGettingRecipeDetails(unittest.TestCase):
	def test_get_recipe(self):
		recipe_id = 'Easy-French-Onion-Soup-2038937'
		expected_recipe_result = 200
		response = get_recipe(recipe_id)
		self.assertEqual(expected_recipe_result, response.status_code)


"""
Test methods related to retrieving ingredient list for a recipe and scaling
"""
class TestGetScaledIngredients(unittest.TestCase):

	# Test getting an ingredient list and servingsfor a recipe given a recipe
	# id
	def test_get_ingredients_and_servings(self):
		recipe_id = 'Easy-French-Onion-Soup-2038937'
		expected_ingredients_list = ['3 tablespoons butter',
									 '3 onions (medium, thinly sliced)',
									 '1 package au jus gravy mix (McCormick®)',
									 '3 cups water']
		expected_servings = 4
		actual_ingredients, actual_servings = get_ingredients_and_servings(recipe_id)
		# self.assertEqual(expected_ingredients_list, actual_ingredients)
		# self.assertEqual(expected_servings, actual_servings)



if __name__ == '__main__':
	unittest.main()