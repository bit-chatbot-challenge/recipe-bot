"""
This is the test suite for the wrapper for methods related to the Yummly API.
"""
import unittest
from unittest import mock
from api_functions import get_recipe_info
from request_error import RequestError
from no_match_error import NoMatchError

"""
Mock for requests.get
"""
def mocked_requests_get(*args, **kwargs):
	class MockedResponse:
		def __init__(self, status_code, json_data):
			self.status_code = status_code
			self.json_data = json_data

		def json(self):
			return self.json_data

	if 'params' in kwargs:
		params = kwargs.get('params')
		if params['q'] == 'butterbeer':
			return MockedResponse(500, None)
		elif params['q'] == 'hamster food':
			mock_json_data = { 'criteria': { 'excludedIngredient': None, 
									 	 	 'q': 'hamster food', 
									 	 	 'allowedIngredient': None
								   	   	   }, 
					   	   'totalMatchCount': 0, 
					       'matches': [],
					  	   'attribution': { 'html': "Recipe search powered by <a href='http://www.yummly.co/recipes'><img alt='Yummly' src='https://static.yummly.co/api-logo.png'/></a>",
											'logo': 'https://static.yummly.co/api-logo.png',
											'url': 'http://www.yummly.co/recipes/',
											'text': 'Recipe search powered by Yummly'
									  	  }, 
					   	   'facetCounts': {}}
			return MockedResponse(200, mock_json_data)

	if args[0] == 'http://api.yummly.com/v1/api/recipes':
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
		return MockedResponse(200, mock_json_data)
	elif args[0] == 'http://api.yummly.com/v1/api/recipe/Easy-French-Onion-Soup-2038937':
		mock_recipe_data = { 'numberOfServings': 4, 
		  				  	   'rating': 3, 
		  				  	   'flavors': {}, 
		  				  	   'ingredientLines': [ '3 tbsps butter', 
		  					   				   		'3 medium onions, thinly sliced', 
		  					   				   		'1 package McCormick® Au Jus Gravy Mix', 
		  					   				   		'3 cups water' ], 
		  				  	   'yield': None, 
		  				  	   'name': 'Easy French Onion Soup', 
		  				  	   'totalTimeInSeconds': 2100, 
		  				  	   'source': { 'sourceDisplayName': 'McCormick', 
		  			  				       'sourceRecipeUrl': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup', 
		  			  				  	   'sourceSiteUrl': 'http://www.mccormick.com' }, 
		  				  	   'nutritionEstimates': [ { 'unit': {'pluralAbbreviation': 'kcal', 
		  									 				 	  'plural': 'calories', 
		  									 				 	  'id': 'fea252f8-9888-4365-b005-e2c63ed3a776', 
		  									 				 	  'name': 'calorie', 
		  									 				 	  'decimal': True, 
		  									 				 	  'abbreviation': 'kcal'}, 
		  												'description': None, 
		  												'value': 80.0, 
		  												'attribute': 'FAT_KCAL' },
		  						  				  	   { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  				  	   'plural': 'grams', 
		  						  			  				  	   'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  				  	   'name': 'gram', 
		  						  			  				  	   'decimal': True, 
		  						  			  				  	   'abbreviation': 'g' },
		  						  						 'description': 'Potassium, K', 
		  						  						 'value': 0.12, 
		  						  						 'attribute': 'K' }, 
		  						  				 	   { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			 				 	   'plural': 'grams', 
		  						  			 				       'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			 				       'name': 'gram', 
		  						  			 			 'decimal': True, 
		  						  			 			 'abbreviation': 'g' }, 
		  						  						 'description': 'Fluoride, F', 
		  						  						 'value': 0.0, 
		  						  						 'attribute': 'FLD' }, 
		  						  					   { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  					   'plural': 'grams', 
		  						  			  					   'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  					   'name': 'gram', 
		  						  			  					   'decimal': True, 
		  						  			  					   'abbreviation': 'g' }, 
		  						  						 'description': 'Phytosterols', 
		  						  						 'value': 0.01, 
		  						  						 'attribute': 'PHYSTR' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': 'Beta-sitosterol', 
		  						  	'value': 0.0, 
		  						  	'attribute': 'SITSTR' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '18:1 c', 
		  						  	'value': 1.81, 
		  						  	'attribute': 'F18D1C' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '18:2 n-6 c,c', 
		  						  	'value': 0.21, 
		  						  	'attribute': 'F18D2CN6' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8',
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': 'Fatty acids, total saturated', 
		  						  	'value': 5.43, 
		  						  	'attribute': 'FASAT' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'mcg_DFE', 
		  						  			  'plural': 'mcg_DFE', 
		  						  			  'id': '4d783ee4-aa07-4958-84bf-3f4b528049dc', 
		  						  			  'name': 'mcg_DFE', 
		  						  			  'decimal': False, 
		  						  			  'abbreviation': 'mcg_DFE' }, 
		  						  	'description': 'Folate, DFE', 
		  						  	'value': 15.99, 
		  						  	'attribute': 'FOLDFE' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '12:0', 
		  						  	'value': 0.32, 
		  						  	'attribute': 'F12D0' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g'}, 
		  						  	'description': 'Glucose (dextrose)', 
		  						  	'value': 1.65, 
		  						  	'attribute': 'GLUS' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '16:1 undifferentiated', 
		  						  	'value': 0.11, 
		  						  	'attribute': 'F16D1' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '18:1 t', 
		  						  	'value': 0.32, 
		  						  	'attribute': 'F18D1T' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': 'Folate, food', 
		  						  	'value': 0.0, 
		  						  	'attribute': 'FOLFD' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'kcal', 
		  						  			  'plural': 'calories', 
		  						  			  'id': 'fea252f8-9888-4365-b005-e2c63ed3a776', 
		  						  			  'name': 'calorie', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'kcal' }, 
		  						  	'description': 'Energy', 
		  						  	'value': 456.34, 
		  						  	'attribute': 'ENERC_KJ' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  				'plural': 'grams', 
		  						  				'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  				'name': 'gram', 
		  						  				'decimal': True, 
		  						  				'abbreviation': 'g' }, 
		  						  	'description': '4:0', 
		  						  	'value': 0.32, 
		  						  	'attribute': 'F4D0' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	  'description': 'Fructose', 
		  						  	  'value': 0.83, 
		  						  	  'attribute': 'FRUS' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Vitamin E (alpha-tocopherol)', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'TOCPHA' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	 	'description': 'Water', 
		  						  	 	'value': 290.38, 
		  						  	 	'attribute': 'WATER' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': '8:0', 
		  						  	   'value': 0.11, 
		  						  	   'attribute': 'F8D0' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Retinol', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'RETOL' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Sugars, total', 
		  						  	   'value': 3.3, 
		  						  	   'attribute': 'SUGAR' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': '6:0', 
		  						  	   'value': 0.21, 
		  						  	   'attribute': 'F6D0' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Fatty acids, total monounsaturated', 
		  						  	   'value': 2.24, 
		  						  	   'attribute': 'FAMS' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Ash', 
		  						  	   'value': 0.21, 
		  						  	   'attribute': 'ASH' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Selenium, Se', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'SE' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Fiber, total dietary', 
		  						  	   'value': 1.65, 
		  						  	   'attribute': 'FIBTG' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Protein', 
		  						  	   'value': 0.93, 
		  						  	   'attribute': 'PROCNT' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Carbohydrate, by difference', 
		  						  	   'value': 7.43, 
		  						  	   'attribute': 'CHOCDF' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Folate, total', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'FOL' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Vitamin K (phylloquinone)', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'VITK' }, 
		  						  	   {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '18:0', 'value': 1.07, 'attribute': 'F18D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Lutein + zeaxanthin', 'value': 0.0, 'attribute': 'LUT+ZEA'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Cholesterol', 'value': 0.02, 'attribute': 'CHOLE'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '17:0', 'value': 0.11, 'attribute': 'F17D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Phosphorus, P', 'value': 0.03, 'attribute': 'P'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Choline, total', 'value': 0.01, 'attribute': 'CHOLN'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '10:0', 'value': 0.32, 'attribute': 'F10D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Calcium, Ca', 'value': 0.03, 'attribute': 'CA'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Magnesium, Mg', 'value': 0.01, 'attribute': 'MG'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Fatty acids, total polyunsaturated', 'value': 0.32, 'attribute': 'FAPU'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '14:0', 'value': 0.75, 'attribute': 'F14D0'}, {'unit': {'pluralAbbreviation': 'mcg_RAE', 'plural': 'mcg_RAE', 'id': '0fcf76b3-891a-403d-883f-58c8809ef151', 'name': 'mcg_RAE', 'decimal': False, 'abbreviation': 'mcg_RAE'}, 'description': 'Vitamin A, RAE', 'value': 72.85, 'attribute': 'VITA_RAE'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '16:0', 'value': 2.34, 'attribute': 'F16D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '18:1 undifferentiated', 'value': 2.13, 'attribute': 'F18D1'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '18:2 undifferentiated', 'value': 0.32, 'attribute': 'F18D2'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Sucrose', 'value': 0.83, 'attribute': 'SUCS'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Carotene, beta', 'value': 0.0, 'attribute': 'CARTB'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '16:1 c', 'value': 0.11, 'attribute': 'F16D1C'}, {'unit': {'pluralAbbreviation': 'IU', 'plural': 'IU', 'id': 'ed46fe0c-44fe-4c1f-b3a8-880f92e30930', 'name': 'IU', 'decimal': True, 'abbreviation': 'IU'}, 'description': 'Vitamin A, IU', 'value': 267.79, 'attribute': 'VITA_IU'}, {'unit': {'pluralAbbreviation': 'kcal', 'plural': 'calories', 'id': 'fea252f8-9888-4365-b005-e2c63ed3a776', 'name': 'calorie', 'decimal': True, 'abbreviation': 'kcal'}, 'description': 'Energy', 'value': 109.36, 'attribute': 'ENERC_KCAL'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Vitamin C, total ascorbic acid', 'value': 0.01, 'attribute': 'VITC'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Total lipid (fat)', 'value': 8.63, 'attribute': 'FAT'}, {'unit': {'pluralAbbreviation': 'IU', 'plural': 'IU', 'id': 'ed46fe0c-44fe-4c1f-b3a8-880f92e30930', 'name': 'IU', 'decimal': True, 'abbreviation': 'IU'}, 'description': 'Vitamin D', 'value': 6.39, 'attribute': 'VITD-'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Sodium, Na', 'value': 0.07, 'attribute': 'NA'}], 'id': 'Easy-French-Onion-Soup-2038937', 'attribution': {'url': 'http://www.yummly.co/recipe/Easy-French-Onion-Soup-2038937', 'logo': 'https://static.yummly.co/api-logo.png', 'html': "<a href='http://www.yummly.co/recipe/Easy-French-Onion-Soup-2038937'>Easy French Onion Soup recipe</a> information powered by <img alt='Yummly' src='https://static.yummly.co/api-logo.png'/>", 'text': 'Easy French Onion Soup recipes: information powered by Yummly'}, 'images': [{'imageUrlsBySize': {'360': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s360-c', '90': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s90-c'}, 'hostedMediumUrl': 'https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s180', 'hostedLargeUrl': 'https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s360', 'hostedSmallUrl': 'https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s90'}], 'totalTime': '35 min', 'attributes': {'course': ['Soups']}}
		return MockedResponse(200, mock_recipe_data)

"""
Test the wrapper method for retreiving info from the API
"""
#Patch requests.get to mock API call
@mock.patch('api_functions.requests.get', side_effect=mocked_requests_get)
class TestAPIWrapper(unittest.TestCase):

	def setUp(self):
		self.search_term = 'onion soup'

	# Test the wrapper method for a simple search: one search term, no options,
	# no scaling
	def test_api_wrapper_simple(self, mock_get):
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

	# Test the wrapper method for a simple search: one search term, no options,
	# scaling
	def test_api_wrapper_scaling(self, mock_get):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '9.0 tbsps butter',
									  				 	 '9.0 medium onions, thinly sliced',
									  				 	 '3.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '9.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 12
		recipe_info = get_recipe_info(self.search_term, desired_servings)
		self.assertEqual(expected_recipe_info, recipe_info)

	# Test the wrapper method for a search with an allergy requirement
	def test_api_wrapper_allergy(self, mock_get):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '3.0 tbsps butter',
									  				 	 '3.0 medium onions, thinly sliced',
									  				 	 '1.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '3.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 4
		allergy = 'Gluten-Free'
		recipe_info = get_recipe_info(self.search_term, desired_servings, allergy=allergy)
		self.assertEqual(expected_recipe_info, recipe_info)

	# Test the wrapper method for a search with a time requirement
	def test_api_wrapper_time(self, mock_get):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '3.0 tbsps butter',
									  				 	 '3.0 medium onions, thinly sliced',
									  				 	 '1.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '3.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 4
		time = '5400'
		recipe_info = get_recipe_info(self.search_term, desired_servings, time=time)
		self.assertEqual(expected_recipe_info, recipe_info)

	# Test the wrapper method for a search with multiple requirements
	def test_api_wrapper_multi_req(self, mock_get):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '3.0 tbsps butter',
									  				 	 '3.0 medium onions, thinly sliced',
									  				 	 '1.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '3.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 4
		allergy = 'Gluten-Free'
		time = '5400'
		recipe_info = get_recipe_info(self.search_term, desired_servings,
									  allergy=allergy, time=time)
		self.assertEqual(expected_recipe_info, recipe_info)

	# Test the wrapper method for a search with multiple values for one
	# requirement
	def test_api_wrapper_req_multi(self, mock_get):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '3.0 tbsps butter',
									  				 	 '3.0 medium onions, thinly sliced',
									  				 	 '1.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '3.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 4
		allergy = ['Gluten-Free', 'Seafood-Free']
		recipe_info = get_recipe_info(self.search_term, desired_servings,
									  allergy=allergy)
		self.assertEqual(expected_recipe_info, recipe_info)

	# Test the wrapper method for a search with an excluded ingredient
	def test_api_wrapper_excluded(self, mock_get):
		expected_recipe_info = { 'name': 'Easy French Onion Soup',
							 	 'scaled_ingredients': [ '3.0 tbsps butter',
									  				 	 '3.0 medium onions, thinly sliced',
									  				 	 '1.0 package McCormick® Au Jus Gravy Mix',
									  				 	 '3.0 cups water' ],
							 	 'recipe_url': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup',
						   		  }
		desired_servings = 4
		excluded_ingredient = 'thyme'
		recipe_info = get_recipe_info(self.search_term, desired_servings,
									  excluded_ingredient=excluded_ingredient)
		self.assertEqual(expected_recipe_info, recipe_info)


"""
Test that the wrapper method for retreiving info from the API raises exceptions
"""
#Patch requests.get to mock API call
@mock.patch('api_functions.requests.get', side_effect=mocked_requests_get)
class TestAPIWrapperExceptions(unittest.TestCase):

	def setUp(self):
		self.desired_servings = 4

	# Test that RequestError is raised if an error is returned for the search
	# request
	def test_requesterror_search(self, mock_get):
		server_search_term = 'butterbeer'
		self.assertRaises(RequestError, get_recipe_info, server_search_term,
						  self.desired_servings)

	# Test that NoMatchError is raised if no matches are returned for the search
	# request
	def test_nomatcherror_search(self, mock_get):
		no_match_search_term = 'hamster food'
		self.assertRaises(NoMatchError, get_recipe_info, no_match_search_term,
						  self.desired_servings)

if __name__ == '__main__':
	unittest.main()