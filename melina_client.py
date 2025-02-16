import json
import requests


def handle(message: str):
    if message.startswith('cabp'):
        note = message.replace('cabp', '')
        response = requests.post(url="http://localhost:8090/ca/boot-plan/make",
                                 data=json.dumps({'note': note}),
                                 headers={'Content-Type': 'application/json'})
