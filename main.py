"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import os

from oura.ouraauth import OuraClient
from dotenv import load_dotenv
import time


class DoRequests:
    def __init__(self):
        pass

    def insert_db(self):
        pass

    def update_db(self):
        pass

    def set_environment(self):
        # Todo load from db
        #    and .env file
        pass

    def setup_client(self):
        env = {
            'client_id': '',
            'client_secret': '',
            'access_token': '',
            'refresh_token': '',
            'refresh_callback': ''
        }

        oauth = OuraClient(
            client_id=None,
            client_secret=None,
            access_token=None,
            refresh_token=None,
            refresh_callback=None
        )

        return oauth

def main():



if __name__ == '__main__':
    main()
