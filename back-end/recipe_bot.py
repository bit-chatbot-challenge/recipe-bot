"""
This is the AWS Lambda function that handles recipe requests given to the
recipe Lex bot.
"""

from __future__ import print_function
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ALLERGIES = []
ALLERGIES_LIST = {
    'dairy free': 'Dairy-Free',
    'egg free': 'Egg-Free',
    'peanut free': 'Peanut-free',
    'tree nut free': 'Tree Nut-Free',
    'gluten free': 'Gluten-Free',
    'seafood free': 'Seafood-Free',
    'sesame free': 'Sesame-Free',
    'soy free': 'Soy-free',
    'sulfite free': 'Sulfite-Free',
    'wheat free': 'Wheat-Free'
}
RESTRICTIONS = []

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


def validate_restrictions(restriction):
    """
    Called by find_recipe to validate slot data of request.
    """
    # If a slot is null, validation fails and returns prompt to elicit slot
    if restriction != 'No' and restriction is not None:
        if restriction in ALLERGIES_LIST:
            ALLERGIES.append(ALLERGIES_LIST[restriction])
        else:
            RESTRICTIONS.append(restriction)
        return build_validation_result(False,
                                       'Restrictions',
                                       'Are there any more dietary restrictions or allergies I should know about?')
    return build_validation_result(True, None, None)



def parse_time(time_slot):
    """
    Utility function for converting Amazon duration values to seconds.
    Doesn't work for values that include years, months, weeks.
    """
    convert = {
        'D': lambda x: 24*60*60*x,
        'H': lambda x: 60*60*x,
        'M': lambda x: 60*x,
        'S': lambda x: x
    }
    seconds = 0
    for i, c in enumerate(time_slot):
        if c.isdigit() and  (time_slot[i-1].isalpha() or i == 0):
            if time_slot[i+1].isdigit():
                seconds += convert[time_slot[i+2]](int(time_slot[i:i+2]))
            else:
                seconds += convert[time_slot[i+1]](int(c))
        else:
            pass
    return seconds


def parse_api_response(response):
    return response


def find_recipe(intent_request):
    """
    Called by dispatch to handle a recipe request intent.
    """
    # Get invocation source
    source = intent_request['invocationSource']
    # If source is DialogCodeHook, validate our slots
    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = validate_restrictions(slots["Restrictions"])
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        
        # Return attributes and slots back to bot for the next step
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    # Right here is where we would need to make an API call to retrieve a recipe
    # For now just a simple response, will write template function later
    # Fulfill recipe intent and returned adjusted recipe
    response = 'placeholdin it up over here'
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText', 'content': parse_api_response(response)})

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


def handler(event, contex):
    """
    Handle incoming recipe requests by passing event to dispatch function
    """
    # Print request contents
    print("Received recipe request: " + json.dumps(event, indent=2))
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)
