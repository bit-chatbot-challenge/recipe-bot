import unittest
from recipe_bot import *

class TestRecipeBot(unittest.TestCase):
    def setUp(self):
        self.details = {
            'name': 'Baked Bacon Mac & Cheese',
            'recipe_url': 'https://notarealurl.com',
            'scaled_ingredients': [
                '6 lbs of bacon',
                '10 lbs. of cheddar',
                '5 bags of macaroni noodles'
            ]
        }
        self.slots = {
            'RecipeType': 'lasagna',
            'Servings': 6,
            'Restrictions': 'lactose intolerant',
            'RecipeTime': 'PT20M'
        }

    def test_get_slots(self):
        test = {
            "currentIntent": {
                "name": "intent-name",
                "slots": self.slots
            }
        }
        self.assertEqual(get_slots(test), self.slots)

    def test_elicit_slot(self):
        params = {
            'session_attributes': {
                'test': 123
            },
            'intent_name': 'FindRecipe',
            'slots': self.slots,
            'slot_to_elicit': 'Servings',
            'message': 'How many are you feeding?'
        }
        expected = {
            'sessionAttributes': params['session_attributes'],
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': params['intent_name'],
                'slots': params['slots'],
                'slotToElicit': params['slot_to_elicit'],
                'message': params['message']
            }
        }
        self.assertEqual(expected, elicit_slot(params['session_attributes'],
                                               params['intent_name'],
                                               params['slots'],
                                               params['slot_to_elicit'],
                                               params['message']))

    def test_close(self):
        params = {
            'session_attributes': {

            },
            'fulfillment_state': 'Fullfilled',
            'message': 'Here is your requested recipe'
        }
        expected = {
            'sessionAttributes': params['session_attributes'],
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': params['fulfillment_state'],
                'message': params['message']
            }
        }
        self.assertEqual(expected, close(params['session_attributes'],
                                         params['fulfillment_state'],
                                         params['message']))

    def test_delegate(self):
        params = {
            'session_attributes': {
                'test': 123
            },
            'slots': self.slots
        }
        expected = {
            'sessionAttributes': params['session_attributes'],
            'dialogAction': {
                'type': 'Delegate',
                'slots': params['slots']
            }
        }

        self.assertEqual(expected, delegate(params['session_attributes'],
                                            params['slots']))


    def test_build_validation_result(self):
        params = {
            'is_valid': False,
            'violated_slot': 'Servings',
            'message_content': None
        }
        expected = {
            'isValid': params['is_valid'],
            'violatedSlot': params['violated_slot']
        }
        self.assertEqual(expected, build_validation_result(params['is_valid'],
                                                           params['violated_slot'],
                                                           params['message_content']))
        params['message_content'] = 'How many are you feeding?'
        expected['message'] = {'contentType': 'PlainText', 'content': params['message_content']}
        self.assertEqual(expected, build_validation_result(params['is_valid'],
                                                           params['violated_slot'],
                                                           params['message_content']))

    def test_validate_restrictions(self):
        expected = build_validation_result(False,
                                            'Restrictions',
                                            'Are there any more dietary restrictions or' \
                                            ' allergies I should know about?')
        expected2 = build_validation_result(True, None, None)
        test = validate_restrictions('gluten free')
        test2 = validate_restrictions('No')
        test3 = validate_restrictions('cheese')
        self.assertEqual(expected, test)
        self.assertTrue('Gluten-Free' in ALLERGIES)
        self.assertEqual(expected2, test2)
        self.assertEqual(expected, test3)
        self.assertTrue('cheese' in RESTRICTIONS)


    def test_parse_time(self):
        ten_minutes = 'PT10M'
        five_hours = 'PT5H'
        three_days = 'P3D'
        forty_five_seconds = 'PT45S'
        five_hours_ten_minutes = 'PT5H10M'
        self.assertEqual('600', parse_time(ten_minutes))
        self.assertEqual('18000', parse_time(five_hours))
        self.assertEqual('259200', parse_time(three_days))
        self.assertEqual('45', parse_time(forty_five_seconds))
        self.assertEqual('18600', parse_time(five_hours_ten_minutes))
    
    def test_get_bot_response(self):
        name = self.details['name']
        ingredients = self.details['scaled_ingredients']
        url = self.details['recipe_url']
        expected = f'Here is a recipe called {name}. ' \
                   f'The full instructions are available at: {url}. \n' \
                   'Based on the desired servings, you will need: \n' \
                   f'- {ingredients[0]} \n' \
                   f'- {ingredients[1]} \n' \
                   f'- {ingredients[2]} \n'
        self.assertEqual(expected, get_bot_response(self.details))

    def test_find_recipe(self):
        intent = {
            'currentIntent': {
                'name': 'FindRecipe',
                'slots': self.slots
            },
            'invocationSource': 'DialogCodeHook',
            'sessionAttributes': {
                'test': 123
            }
        }
        slots = intent['currentIntent']['slots']
        validation_result = validate_restrictions(slots['Restrictions'])
        expected = elicit_slot(
            intent['sessionAttributes'],
            intent['currentIntent']['name'],
            slots,
            validation_result['violatedSlot'],
            validation_result['message']
        )
        self.assertEqual(expected, find_recipe(intent))


if __name__ == '__main__':
    unittest.main()
