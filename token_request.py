import os
from oura.ouraauth import OuraOAuth2
from flask import Flask, request, redirect, session, url_for
from dotenv import load_dotenv
import logging

load_dotenv()
from db_stuff import DataBaseOura


app = Flask(__name__)
app.secret_key = os.urandom(24)

logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return '<h1>HOME</h1>'


@app.route('/auth')
def browser_auth():
    url, state = auth_client.authorize_endpoint(
        redirect_uri='http://127.0.0.1:5353/callback')
    # session['oauth_state'] = state
    return redirect(url)


@app.route('/callback')
def callback():
    auth_response = request.url
    auth_state = request.args.get('state')
    session['oauth_state'] = request.args.get('state')
    auth_code = request.args.get('code')
    auth_error = request.args.get('error')

    print('code:', auth_code, 'state:', auth_state)
    aa = True if auth_state is session['oauth_state'] else False
    print(aa)

    try:
        # Get the token
        token_dict = auth_client.fetch_token(auth_response=auth_response)
        print('Save these values')
        for key, value in token_dict.items():
            # Todo remove printing the tokens out.
            #   append to file instead
            print('{} = {}'.format(key, value))
        # Todo insert token and state into db
    except Exception as e:
        print(e)
        logging.exception(e)
    else:
        session['oauth_token'] = token_dict
        user_info = DataBaseOura().get_user_info(OURA_CLIENT_ID, OURA_CLIENT_SECRET, token_dict['access_token'],
                                                 token_dict['refresh_token'])
        print(user_info)

        DataBaseOura().insert_into(email=user_info['email'], oura_token=token_dict)
        return '<h1>All done! You can close this window.</h1>'
    finally:
        if auth_error:
            print('Access Denied')
            logging.error(auth_error)

        return redirect(url_for('home'))


if __name__ == '__main__':
    d = DataBaseOura()
    OURA_CLIENT_ID = os.getenv('OURA_CLIENT_ID')
    OURA_CLIENT_SECRET = os.getenv('OURA_CLIENT_SECRET')
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    auth_client = OuraOAuth2(client_id=OURA_CLIENT_ID,
                             client_secret=OURA_CLIENT_SECRET)

    app.run(debug=True, host='127.0.0.1', port=5353)
