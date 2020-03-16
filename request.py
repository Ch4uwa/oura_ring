"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import os

try:
    from dotenv import load_dotenv
    from requests_oauthlib import OAuth2Session
    import requests
except ImportError as import_error:
    # Expected exceptions
    print(import_error.__class__.__name__ + ': {}'.format(import_error))
except Exception as exception:
    # Unexpected exceptions
    print(exception.__class__.__name__, exception)
else:
    load_dotenv('.env')

client_id = os.getenv('OURA_CLIENT_ID')
client_secret = os.getenv('OURA_CLIENT_SECRET')

authorization_base_url = 'https://cloud.ouraring.com/oauth/authorize'
token_url = 'https://api.ouraring.com/oauth/token'
redirect_uri = 'https://localhost/'

oura = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri)

try:
    _authorization_url, state = oura.authorization_url(authorization_base_url)
except Exception as e:
    print(e)
else:
    session = {'oauth_state': state}

    r = requests.get(_authorization_url)
    print(r.json())
