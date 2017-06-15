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
                                           'RecipeType',
                                           'I did not understand, what kind of recipe do you need?')
        expected2 = build_validation_result(False,
                                            'ServingSize',
                                            'How many people does this need to feed?')
        expected3 = build_validation_result(False,
                                            'Restrictions',
                                            'Are there any dietary restrictions I should know about?')
        expected4 = build_validation_result(False,
                                            'RecipeTime',
                                            'How long should this take to make?')
        expected5 = build_validation_result(True, None, None)

        test = validate_find_recipe(None, 10, None, None)
        test2 = validate_find_recipe('Lasagna', None, None, None)
        test3 = validate_find_recipe('Lasagna', 10, None, None)
        test4 = validate_find_recipe('Lasagna', 10, 'Vegan', None)
        test5 = validate_find_recipe('Lasagna', 10, 'Vegan', 20)

        self.assertEqual(expected, test)
        self.assertEqual(expected2, test2)
        self.assertEqual(expected3, test3)
        self.assertEqual(expected4, test4)
        self.assertEqual(expected5, test5)

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

        recipe_type = get_slots(intent)["RecipeType"]
        serving_size = get_slots(intent)["ServingSize"]
        restrictions = get_slots(intent)["Restrictions"]
        recipe_time = get_slots(intent)["RecipeTime"]

        message = 'Alright, here is a recipe for {}, that feeds {}, and is safe for {}'.format(
                                                                                        recipe_type,
                                                                                        serving_size,
                                                                                        restrictions)
        close_message = {'contentType': 'PlainText', 'content': message}
        expected = close(intent['sessionAttributes'], 'Fulfilled', close_message)

        self.assertEqual(expected, find_recipe(intent))

        intent['currentIntent']['slots']['Restrictions'] = 'None'
        message = 'Alright, here is a recipe for {}, that feeds {}'.format(recipe_type, serving_size)
        close_message = {'contentType': 'PlainText', 'content': message}
        expected = close(intent['sessionAttributes'], 'Fulfilled', close_message)

        self.assertEqual(expected, find_recipe(intent))

        intent['invocationSource'] = 'DialogCodeHook'
        expected = delegate(intent['sessionAttributes'], get_slots(intent))

        self.assertEqual(expected, find_recipe(intent))

        intent['currentIntent']['slots']['Restrictions'] = None
        validation_result = validate_find_recipe(recipe_type,
                                                 serving_size,
                                                 None,
                                                 recipe_time)
        expected = elicit_slot(intent['sessionAttributes'],
                               intent['currentIntent']['name'],
                               get_slots(intent),
                               validation_result['violatedSlot'],
                               validation_result['message'])

        self.assertEqual(expected, find_recipe(intent))

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
