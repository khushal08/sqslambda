import json

import requests


def lambda_handler(event, context):
    for record in event['Records']:
        print(record['body'])
