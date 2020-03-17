"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import os
import logging
try:
    from dotenv import load_dotenv
    from requests_oauthlib import OAuth2Session
except ImportError as import_error:
    # Expected exceptions
    print(import_error.__class__.__name__ + ': {}'.format(import_error))
except Exception as exception:
    # Unexpected exceptions
    print(exception.__class__.__name__, exception)
else:
    load_dotenv('.env')


class Authentication:
    def __init__(self):
        self.client_id = os.getenv('OURA_CLIENT_ID')
        self.client_secret = os.getenv('OURA_CLIENT_SECRET')

        self.base_api = 'https://api.ouraring.com/v1/'
        self.base_url = 'https://cloud.ouraring.com'
        self.response_type = 'token'
        self.authorization_base_url = self.base_url + '/oauth/authorize'
        self.token_url = 'https://api.ouraring.com/oauth/token'
        self.redirect_uri = 'https://example-app.com/callback'  # 'https://127.0.0.1:5353'

        self.oura = OAuth2Session(
            client_id=self.client_id, redirect_uri=self.redirect_uri)

    def authorize_app(self):
        # Ask user to authorize the application
        self.authorization_url, self.state = self.oura.authorization_url(
            self.authorization_base_url)

        print(self.authorization_url)

        response = self.oura.get(self.authorization_url)
        print(response)
        # self.response = input('Response URL:')

    def get_token(self):

        self.token = self.oura.fetch_token(
            self.token_url, authorization_response=self.response, client_secret=self.client_secret)

        # self.token = 'TXOQ4B4C4LURQ7ZG7NG7UMUZOKRMH33X'  # This token is for testing
        return self.token

    def api_call(self, token):
        _token = token
        _scope = 'userinfo'
        self.api_url = self.base_api + '{}?access_token={}'.format(_scope,
                                                                   _token)
        r = self.oura.get(self.api_url)
        print(r.text)

        return r


def main():
    a = Authentication()
    a.authorize_app()

if __name__ == '__main__':
    main()
