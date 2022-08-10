import os
import requests
from tqdm import tqdm

# define function to get a new access token
def get_access_token(client_id, client_secret, authorization_code):
 
    oauth_url = "https://www.strava.com/oauth/token"
 
    payload = {
        "client_id": client_id, 
        "client_secret": client_secret, 
        "code": authorization_code,
        "grant_type": "authorization_code",
        "f": "json", 
    }
 
    r = requests.post(oauth_url, data=payload, verify=False)
 
    access_token = r.json()["access_token"]
    return access_token

def get_data(access_token, per_page=200, page=1):

    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"per_page": per_page, "page": page}

    data = requests.get(
        activities_url, 
        headers=headers, 
        params=params
    ).json()

    return data

if __name__ == "__main__":
    # set strava variables
    client_id = os.environ['STRAVA_CLIENT_ID']
    client_secret = os.environ['STRAVA_CLIENT_SECRET']
    authorization_code = os.environ['STRAVA_AUTH_CODE']

    # Go to the following link and copy the auth code to the local .env file
    # https://www.strava.com/oauth/authorize?client_id=15880&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read


    access_token = get_access_token(client_id, client_secret, authorization_code)

    max_number_of_pages = 10
    data = list()
    for page_number in tqdm(range(1, max_number_of_pages + 1)):
        page_data = get_data(access_token, page=page_number)
        if page_data == []:
            break

        data.append(page_data)