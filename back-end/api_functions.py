"""
This module contains the functionality needed to query the Yummly API.
"""

import requests
import os
import logging
import re
from collections import OrderedDict
from request_error import RequestError
from no_match_error import NoMatchError

""" --- Constants ---"""
HEADERS  = OrderedDict({
	'X-Yummly-App-ID': os.environ["AWS_YUMMLY_APP_ID"],
	'X-Yummly-App-Key': os.environ['AWS_YUMMLY_APP_KEY'],
})

AUTH_PARAMETERS = OrderedDict({
	'_app_id': os.environ["AWS_YUMMLY_APP_ID"],
	'_app_key': os.environ['AWS_YUMMLY_APP_KEY'],
})

OPTIONAL_PARAMETERS = ['allergy', 'time', 'excluded_ingredient']

YUMMLY_PARAM_MAPPING = {
	'allergy': 'allowedAllergy[]',
	'time': 'maxTotalTimeInSeconds',
	'excluded_ingredient': 'excludedIngredient[]',
}

BASE_API_SEARCH_URL = 'http://api.yummly.com/v1/api/recipes'

BASE_URL = 'http://www.yummly.com/recipe/'

BASE_API_GET_URL = 'http://api.yummly.com/v1/api/recipe/'


"""
Method to add optional parameters to payload of parameters for search
"""
def add_optional_parameters(payload, additional_params):
	for option in OPTIONAL_PARAMETERS:
		if option in additional_params:
			api_param_name = YUMMLY_PARAM_MAPPING[option]
			payload[api_param_name] = additional_params[option]
	return payload

"""
Method to create payload of parameters for search
"""
def create_payload(search_term, **options):
	payload = { 'q': search_term }
	if options:
		payload = add_optional_parameters(payload, options)
	return payload

"""
Method to query Yummly API for recipe based on received parameters
"""
def get_search_results(search_term, **options):
	log_api_event('query', search_term, **options)
	payload = create_payload(search_term, **options)
	r = requests.get(BASE_API_SEARCH_URL, headers=HEADERS, params=payload)
	r.connection.close()
	return r


"""
Method to parse response from Yummly API: if the response has a non 200
status code, log and return the error; if the response has a 200 status code 
and the keyword is 'search', log and return the id of the first matching
recipe; if the response has a 200 status code and the keyword is 'recipe', log
and return the response body
"""
def parse_response(keyword, response):
	if response.status_code == 200:
		if keyword == 'search':
			json_response = response.json()
			if not json_response['matches']:
				search_term = json_response['criteria']['q']
				del json_response['criteria']['q']
				raise NoMatchError(search_term, **json_response['criteria'])
			else:
				recipe_id = json_response['matches'][0]['id']
				log_api_event('parsed search result', recipe_id)
			return recipe_id
		elif keyword == 'recipe':
			log_api_event('parsed recipe result')
			return response.json()
	else:
		raise RequestError(response.status_code)

"""
Method to get recipe based on recipe id
"""
def get_recipe(recipe_id):
	log_api_event('get recipe', recipe_id)
	recipe_base_url = BASE_API_GET_URL + recipe_id
	r = requests.get(recipe_base_url, params=AUTH_PARAMETERS)
	r.connection.close()
	return r

"""
Method to get name of a recipe
"""
def get_recipe_name(recipe_response):
	log_api_event('retrieve name')
	return recipe_response['name']

"""
Method to get ingredients list for a recipe
"""
def get_scaled_ingredients(recipe_response, desired_servings):
	log_api_event('scaling')
	ingredients = recipe_response['ingredientLines']
	original_servings = recipe_response['numberOfServings']
	scaled_ingredients = []
	for ingredient in ingredients:
		if not re.match('\d+', ingredient):
			scaled_ingredients.append(ingredient)
		else:
			quantity = re.match('\d+', ingredient).group()
			unit = re.sub('\s', '', re.split('\d+', ingredient)[1], count=1)
			scaled_quantity = (desired_servings/original_servings)*int(quantity)
			scaled_ingredients.append(str(scaled_quantity) + ' ' + unit)
	return scaled_ingredients

"""
Method to create URL for user to view in browser
"""
def get_recipe_url(recipe_response):
	log_api_event('retrieve url')
	return recipe_response['source']['sourceRecipeUrl']

"""
Method to get details of a recipe: returns name, list of scaled ingredients, 
and recipe URL
"""
def get_recipe_details(recipe_response, desired_servings):
	log_api_event('get recipe details')
	details = {}
	details['name'] = get_recipe_name(recipe_response)
	details['scaled_ingredients'] = get_scaled_ingredients(recipe_response, desired_servings)
	details['recipe_url'] = get_recipe_url(recipe_response)
	return details


"""
Wrapper method to search API and get recipe details based on provided info
"""
def get_recipe_info(search_term, desired_servings):
	search_response = get_search_results(search_term)
	try:
		matching_recipe_id = parse_response('search', search_response)
	except RequestError as request_err:
		log_api_error(request_err.message())
		raise request_err
	except NoMatchError as match_err:
		log_api_error(match_err.message())
		raise match_err
	recipe_response = get_recipe(matching_recipe_id)
	try:
		matching_recipe = parse_response('recipe', recipe_response)
	except RequestError as request_err:
		log_api_error(request_err.message())
		raise request_err
	matching_recipe_details = get_recipe_details(matching_recipe, desired_servings)
	return matching_recipe_details

"""
Method to log events related to API functionality
"""
def log_api_event(keyword, *term, **criteria):
	if keyword == 'query':
		base_log_message = 'Querying for ' + term[0] + ' recipes'
		if criteria:
			log_message = base_log_message + ' with the following search criteria: ' + str(criteria)
		else:
			log_message = base_log_message
		logging.debug(log_message)
	elif keyword == 'parsed search result':
		log_message = 'Found matching recipe with id ' + term[0]
		logging.debug(log_message)
	elif keyword == 'retrieve url':
		log_message = 'Retrieving url for recipe'
		logging.debug(log_message)
	elif keyword == 'get recipe':
		log_message = 'Getting recipe with id ' + term[0]
	elif keyword == 'get recipe details':
		log_message = 'Getting details for recipe'
		logging.debug(log_message)
	elif keyword == 'scaling':
		log_message = 'Getting and scaling recipe ingredients'
		logging.debug(log_message)
	elif keyword == 'retreive name':
		log_message = 'Getting recipe name'
		logging.debug(log_message)
	elif keyword == 'parsed recipe result':
		log_message = 'Successfuly retreived recipe'
		logging.debug(log_message)

"""
Method to log errors related to API functionality
"""
def log_api_error(error_message):
	logging.error(error_message)
