"""
Martin Karlsson 19-02-2020
"""
import json

from oura.ouraauth import OuraClient, OuraOAuth2
from db_stuff import DataBaseOura
import os
from dotenv import load_dotenv
import dotenv

load_dotenv()


def set_environment(env_file):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, env_file)
    with open(full_path) as file:
        env = json.load(file)
        os.environ['OURA_CLIENT_ID'] = env['client_id']
        os.environ['OURA_CLIENT_SECRET'] = env['client_secret']
        os.environ['OURA_ACCESS_TOKEN'] = env['access_token']
        os.environ['OURA_REFRESH_TOKEN'] = env['refresh_token']


def append_file(filename, token_dict):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename)
    with open(full_path, 'r+') as file:
        prev = json.load(file)
        curr = {
            'client_id': prev.pop('client_id'),
            'client_secret': prev.pop('client_secret'),
            'access_token': token_dict['access_token'],
            'refresh_token': token_dict['refresh_token'],
            'previous': json.dumps(prev)
        }
        file.seek(0)
        json.dump(curr, file)


def get_oura_client(env_file):
    client_id = os.getenv('OURA_CLIENT_SECRET')
    client_secret = os.getenv('OURA_CLIENT_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    refresh_token = os.getenv('REFRESH_TOKEN')
    # refresh_callback = lambda x: append_file(env_file, x)

    auth_client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_callback=lambda x: append_file(env_file, x)
    )

    return auth_client


def main():
    env_file = 'token.json'
    set_environment(env_file)
    client = get_oura_client(env_file)
    user_info = client.user_info()
    print(user_info)


if __name__ == '__main__':
    main()
