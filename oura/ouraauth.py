"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import json

from requests_oauthlib import OAuth2Session


class OuraOAuth2:
    BASE_URL = 'https://cloud.ouraring.com'
    BASE_AUTH_URL = 'https://cloud.ouraring.com/oauth/authorize'
    BASE_TOKEN_URL = 'https://api.ouraring.com/oauth/token'
    SCOPE = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self.session = OAuth2Session(client_id=self.client_id, auto_refresh_url=self.BASE_TOKEN_URL)

    def authorize_endpoint(self, scope=None, redirect_uri=None, **kwargs):
        # Create Authorization url
        self.session.scope = scope or self.SCOPE
        if redirect_uri:
            self.session.redirect_uri = redirect_uri
        return self.session.authorization_url(self.BASE_AUTH_URL, **kwargs)

    def fetch_token(self, auth_response):
        return self.session.fetch_token(
            token_url=self.BASE_TOKEN_URL,
            authorization_response=auth_response,
            client_id=self.client_id,
            client_secret=self.client_secret
        )


class OuraClient:
    API_ENDPOINT = 'https://api.ouraring.com'  # /v1/userinfo/
    BASE_TOKEN_URL = 'https://cloud.ouraring.com/oauth/authorize'

    def __init__(self, client_id, client_secret=None, access_token=None, refresh_token=None, refresh_callback=None):
        self.client_id = client_id
        self.client_secret = client_secret
        token = {}
        if access_token:
            token.update({'access_token': access_token})
        if refresh_token:
            token.update({'refresh_token': refresh_token})

        self._session = OAuth2Session(
            client_id=client_id,
            token=token,
            auto_refresh_url=self.BASE_TOKEN_URL,
            token_updater=refresh_callback
        )

    # Todo Add requests
    def user_info(self):
        url = '{}/v1/userinfo'.format(self.API_ENDPOINT)
        return self._make_request(url=url)

    def activity(self, start=None, end=None):
        """
        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want current day
        :type end: date
        """
        url = self._build_summary_url(start, end, 'activity')
        return self._make_request(url=url)

    def sleep(self, start=None, end=None):
        """
        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want current day
        :type end: date
        """
        url = self._build_summary_url(start, end, 'sleep')
        return self._make_request(url=url)

    def readiness(self, start=None, end=None):
        """
        :param start: Beginning of date range
        :type start: date

        :param end: End of date range, or None if you want current day
        :type end: date
        """
        url = self._build_summary_url(start, end, 'readiness')
        return self._make_request(url=url)

    def _make_request(self, url, data=None, method=None, **kwargs):
        data = data or {}
        method = method or 'GET'
        response = self._session.request(method=method, url=url, data=data, **kwargs)
        if response.status_code == 401:
            self._refresh_token()
            response = self._session.request(method=method, url=url, data=data, **kwargs)

        payload = json.loads(response.content.decode('utf8'))
        return payload

    def _build_summary_url(self, start, end, datatype):
        if start is None:
            raise ValueError('Request for {} summary must include start date.'.format(datatype))

        url = '{0}/v1/{1}?start={2}'.format(self.API_ENDPOINT, datatype, start)
        if end:
            url = '{0}&end={1}'.format(url, end)
        return url

    def _refresh_token(self):
        token = self._session.refresh_token(
            self.BASE_TOKEN_URL, client_id=self.client_id, client_secret=self.client_secret)
        if self._session.token_updater:
            self._session.token_updater(token)

        return token
