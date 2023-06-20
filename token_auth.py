import requests
import requests.auth

import config


def get_token() -> str:
    client_auth = requests.auth.HTTPBasicAuth(config.CLIENT_ID, config.CLIENT_SECRET)
    post_data = {'grant_type': 'password', 'username': config.USERNAME, 'password': config.PASSWORD}
    headers = {'User-Agent': config.USER_AGENT}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data, headers=headers)
    data = response.json()
    return data['access_token']


if __name__=='__main__':
    token = get_token()
