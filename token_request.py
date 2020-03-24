import json
import os
import sys
import threading
from oura.ouraauth import OuraOAuth2
from flask import Flask, request, redirect, session, url_for
from db_stuff import DataBaseOura
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    # Todo Check if access toke is ok before authentication
    return '<h1>HOME</h1>'


@app.route('/auth')
def browser_auth():
    url, state = auth_client.authorize_endpoint(
        redirect_uri='http://127.0.0.1:5353/callback')
    session['oauth_state'] = state
    return redirect(url)


@app.route('/callback')
def callback():
    auth_response = request.url
    auth_state = request.args.get('state')
    auth_code = request.args.get('code')
    print('code:', auth_code, 'state:', auth_state)
    aa = True if auth_state is session['oauth_state'] else False
    print(aa)
    try:
        token_dict = auth_client.fetch_token(auth_response=auth_response)
        print('Save these values')
        for key, value in token_dict.items():
            # Todo remove printing the tokens out.
            #   append to file instead
            print('{} = {}'.format(key, value))
            
    except Exception as e:
        print(e)
    else:
        session['oauth_token'] = token_dict

        return '<h1>All done! You can close this window.</h1>'
    finally:
        if request.args.get('error'):
            print('Access Denied')

    return redirect(url_for('/home'))


if __name__ == '__main__':
    OURA_CLIENT_ID = os.getenv('OURA_CLIENT_ID')
    OURA_CLIENT_SECRET = os.getenv('OURA_CLIENT_SECRET')
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    auth_client = OuraOAuth2(client_id=OURA_CLIENT_ID,
                             client_secret=OURA_CLIENT_SECRET)

    app.secret_key = os.urandom(24)
    app.run(debug=True, host='127.0.0.1', port=5353)
