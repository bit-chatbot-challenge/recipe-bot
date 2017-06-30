"""
This module contains the functionality needed to query the Yummly API.
"""

import requests
import os
import logging
from collections import OrderedDict

""" --- Constants ---"""
HEADERS = OrderedDict({
	'X-Yummly-App-ID': os.environ["AWS_YUMMLY_APP_ID"],
	'X-Yummly-App-Key': os.environ['AWS_YUMMLY_APP_KEY'],
})

OPTIONAL_PARAMETERS = ['allergy', 'time', 'excluded_ingredient']

YUMMLY_PARAM_MAPPING = {
	'allergy': 'allowedAllergy[]',
	'time': 'maxTotalTimeInSeconds',
	'excluded_ingredient': 'excludedIngredient[]',
}


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
	payload = create_payload(search_term, **options)
	r = requests.get('http://api.yummly.com/v1/api/recipes', headers=HEADERS, params=payload)
	r.connection.close()
	log_api_event('query', search_term, **options)
	return r


"""
Method to parse search results from Yummly API
"""
def parse_search_results(response):
	if response.status_code == 500:
		log_api_event('server error')
		return 'server error'
	elif response.status_code == 409:
		log_api_event('rate limit')
		return 'rate limit exceeded'

"""
Method to log events related to API functionality
"""
def log_api_event(keyword, *search_term, **criteria):
	if keyword == 'query':
		base_log_message = 'Querying for ' + search_term[0] + ' recipes'
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