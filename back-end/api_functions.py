"""
This module contains the functionality needed to query the Yummly API.
"""

import requests
import os
import logging
import re
from collections import OrderedDict

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
def add_optional_parameters(params_dict, additional_params):
	for option in OPTIONAL_PARAMETERS:
		if option in additional_params:
			api_param_name = YUMMLY_PARAM_MAPPING[option]
			params_dict[api_param_name] = additional_params[option]
	return params_dict

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
Method to parse search results from Yummly API: if the response has a bad
status code, log and return the error; if the response has a 200 status code,
log and return the id of the first matching recipe
"""
def parse_search_results(response):
	if response.status_code == 500:
		log_api_event('server error')
		return 'server error'
	elif response.status_code == 409:
		log_api_event('rate limit')
		return 'rate limit exceeded'
	elif response.status_code == 400:
		log_api_event('bad request')
		return 'bad request'
	elif response.status_code == 200:
		json_response = response.json()
		recipe_id = json_response['matches'][0]['id']
		log_api_event('parsed result', recipe_id)
		return recipe_id

"""
Method to create URL for user to view in browser
"""
def create_url_for_user(recipe_id):
	log_api_event('generate url', recipe_id)
	return BASE_URL + recipe_id

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
Method to get ingredients list for a recipe
"""
def get_scaled_ingredients(recipe_response, desired_servings):
	log_api_event('scaling')
	ingredients = recipe_response['ingredientLines']
	original_servings = recipe_response['numberOfServings']
	scaled_ingredients = []
	for ingredient in ingredients:
		quantity = re.match('\d+', ingredient).group()
		unit = re.sub('\s', '', re.split('\d+', ingredient)[1], count=1)
		scaled_quantity = (desired_servings/original_servings)*int(quantity)
		scaled_ingredients.append(str(scaled_quantity) + ' ' + unit)
	return scaled_ingredients
	# if response.status_code == 500:
	# 	log_api_event('server error')
	# 	return 'server error'
	# elif response.status_code == 409:
	# 	log_api_event('rate limit')
	# 	return 'rate limit exceeded'
	# elif response.status_code == 400:
	# 	log_api_event('bad request')
	# 	return 'bad request'

"""
Method to get ingredients list and servings for a recipe
"""
def get_ingredients_and_servings(recipe_id):
	# ingredients_list = get_ingredients(r)
	return True, True

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
	elif keyword == 'server error':
		log_message = 'Yummly cannot complete request due to internal server error'
		logging.error(log_message)
	elif keyword == 'rate limit':
		log_message = 'Oops, our bot has exceeded the number of API calls in our plan'
		logging.error(log_message)
	elif keyword == 'bad request':
		log_message = "We are submitting a bad request to the API"
		logging.error(log_message)
	elif keyword == 'parsed result':
		log_message = 'Found matching recipe with id ' + term[0]
		logging.debug(log_message)
	elif keyword == 'generate url':
		log_message = 'Generating url for recipe with id ' + term[0]
		logging.debug(log_message)
	elif keyword == 'get recipe':
		log_message = 'Getting details for recipe with id ' + term[0]
		logging.debug(log_message)
	elif keyword == 'scaling':
		log_message = 'Getting and scaling recipe ingredients'
		logging.debug(log_message)