"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import os
import logging.config
from oura.ouraauth import OuraClient
from dotenv import load_dotenv
import time
from db_stuff import DataBaseOura
import json

load_dotenv()

logging.config.fileConfig(fname='logconf.conf',
                          disable_existing_loggers=False)


def main():
    d = DataBaseOura()
    token = d.get_token(token_id='mrtn.karlsson@gmail.com')

    client = OuraClient(client_id=os.getenv('OURA_CLIENT_ID'), client_secret=os.getenv('OURA_CLIENT_SECRET'),
                        access_token=token['access_token'], refresh_token=token['refresh_token'])

    user_info = client.user_info()
    activity = client.activity(start='2020-03-30')
    readiness = client.readiness(start='2020-03-30')
    sleep = client.sleep(start='2020-03-30')

    d.insert_into(email=user_info['email'], user_info=user_info, sleep=sleep, activity=activity, readiness=readiness)


if __name__ == '__main__':
    main()
