import unittest
from recipe_bot import *

class TestRecipeBot(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_slots(self):
        expected = {
            'RecipeType': 'lasagna',
            'ServingSize': 6,
            'Restrictions': 'lactose intolerant',
            'RecipeTime': 20
        }

        test = {
            "currentIntent": {
                "name": "intent-name",
                "slots": {
                    "RecipeType": "lasagna",
                    "ServingSize": 6,
                    "Restrictions": "lactose intolerant",
                    'RecipeTime': 20
                }
            }
        }

        self.assertEqual(get_slots(test), expected)

    def test_elicit_slot(self):
        params = {
            'session_attributes': {
                'test': 123
            },
            'intent_name': 'FindRecipe',
            'slots': {
                "RecipeType": "lasagna",
                "ServingSize": 6,
                "Restrictions": "lactose intolerant"
            },
            'slot_to_elicit': 'ServingSize',
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
            'slots': {
                "RecipeType": "lasagna",
                "ServingSize": 6,
                "Restrictions": "lactose intolerant",
                'RecipeTime': 20
            }
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
            'violated_slot': 'ServingSize',
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

    def test_validate_find_recipe(self):
        expected = build_validation_result(False,
                                            'Restrictions',
                                            'Are there any more dietary restrictions or allergies I should know about?')
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

        self.assertEqual(600, parse_time(ten_minutes))
        self.assertEqual(18000, parse_time(five_hours))
        self.assertEqual(259200, parse_time(three_days))
        self.assertEqual(45, parse_time(forty_five_seconds))
        self.assertEqual(18600, parse_time(five_hours_ten_minutes))

    def test_find_recipe(self):
        intent = {
            'currentIntent': {
                'name': 'FindRecipe',
                'slots': {
                    "RecipeType": "lasagna",
                    "ServingSize": 6,
                    "Restrictions": "lactose intolerant",
                    'RecipeTime': 20
                }
            },
            'invocationSource': 'FulfillmentCodeHook',
            'sessionAttributes': {
                'test': 123
            }
        }

    def test_dispatch(self):
        intent = {
            'currentIntent': {
                'name': 'FindRecipe',
                'slots': {
                    "RecipeType": "lasagna",
                    "ServingSize": 6,
                    "Restrictions": "lactose intolerant",
                    'RecipeTime': 20
                }
            },
            'invocationSource': 'FulfillmentCodeHook',
            'sessionAttributes': {
                'test': 123
            },
            'userId': 'ralph'
        }

        self.assertEqual(dispatch(intent), find_recipe(intent))

        intent['currentIntent']['name'] = 'whatever'

        self.assertRaises(Exception, lambda: dispatch(intent))


if __name__ == '__main__':
    unittest.main()
