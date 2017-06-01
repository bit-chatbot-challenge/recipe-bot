"""
This is the AWS Lambda function that handles recipe requests given to the
recipe Lex bot.
"""

from __future__ import print_function
import json
import requests

""" --- Main handler --- """

def handler(event, contex):
    """
    Handle incoming recipe requests and return recipe with appropriate
    portions.
    """
    # Print request contents
    print("Received recipe request: " + json.dumps(event, indent=2))
