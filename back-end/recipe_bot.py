"""
This is the AWS Lambda function that handles recipe requests given to the
recipe Lex bot.
"""

from __future__ import print_function
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_slots(intent_request):
    """
    Called by find_recipe to get currently filled slots.
    """
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Called by find_recipe to elicit a missing slot from the user.
    """
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    """
    Called by find_recipe to fulfill a recipe intent request.
    """
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }


def delegate(session_attributes, slots):
    """
    Called by find_recipe to send slots and attributes back to bot.
    """
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Called by validate_find_recipe to format validation results.
    """
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def validate_find_recipe(recipe_type, serving_size, restrictions, recipe_time):
    """
    Called by find_recipe to validate slot data of request.
    """
    # If a slot is null, validation fails and returns prompt to elicit slot
    if recipe_type is None:
        return build_validation_result(False,
                                       'RecipeType',
                                       'I did not understand, what kind of recipe do you need?')

    if serving_size is None:
        return build_validation_result(False,
                                       'ServingSize', 'How many people does this need to feed?')

    if restrictions is None:
        return build_validation_result(False,
                                       'Restrictions',
                                       'Are there any dietary restrictions I should know about?')

    if recipe_time is None:
        return build_validation_result(False,
                                       'RecipeTime',
                                       'How long should this take to make?')

    return build_validation_result(True, None, None)


def find_recipe(intent_request):
    """
    Called by dispatch to handle a recipe request intent.
    """
    # Pull slots from recipe request
    recipe_type = get_slots(intent_request)["RecipeType"]
    serving_size = get_slots(intent_request)["ServingSize"]
    restrictions = get_slots(intent_request)["Restrictions"]
    recipe_time = get_slots(intent_request)["RecipeTime"]
    # Get invocation source
    source = intent_request['invocationSource']

    # If source is DialogCodeHook, validate our slots
    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)

        validation_result = validate_find_recipe(recipe_type, serving_size, restrictions, recipe_time)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Possibly store extra info for Lex
        # Store inside output_session_attributes dict with other session attributes
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        # Return attributes and slots back to bot for the next step
        return delegate(output_session_attributes, get_slots(intent_request))


    # Right here is where we would need to make an API call to retrieve a recipe
    # For now just a simple response, will write template function later
    # If no dietary restrictions, omit from response message
    if restrictions == 'None':
        message = 'Alright, here is a recipe for {}, that feeds {}'.format(recipe_type, serving_size)
    else:
        message = 'Alright, here is a recipe for {}, that feeds {}, and is safe for {}'.format(recipe_type, serving_size, restrictions)

    # Fulfill recipe intent and returned adjusted recipe
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText', 'content': message})

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'FindRecipe':
        return find_recipe(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')




""" --- Main handler --- """
def handler(event, contex):
    """
    Handle incoming recipe requests by passing event to dispatch function
    """
    # Get search results

    # Print request contents
    print("Received recipe request: " + json.dumps(event, indent=2))
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
