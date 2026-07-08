import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test the api"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)


    def handle(self, *args, **kwargs):
        base_url = "http://127.0.0.1:8000/polls"
        url = ''.join([base_url, '/api-token-auth/'])

        response = requests.post(url, json={"username": kwargs["username"], "password": kwargs["password"]})
        token = response.json()['token']

        headers = {
            "Authorization": f"Token {token}"
        }

        # a list questions
        url = ''.join([base_url, '/questions'])
        response = requests.get(url, headers=headers, timeout=(3,30))

        j = response.json()

        detail = j[0]['id']

        url = ''.join([base_url, f'/questions/{detail}'])

        response = requests.get(url, headers=headers, timeout=(3, 30))

        j = response.json()

        print('Finished')