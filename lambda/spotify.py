from requests_oauth2 import OAuth2
import os
oauth2_handler = OAuth2(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'], "https://accounts.spotify.com/", "https://tn78yzlfic.execute-api.us-east-1.amazonaws.com/a/spotify", "authorize", "api/token")
authorization_url = oauth2_handler.authorize_url('user-read-playback-state playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-follow-read user-follow-modify user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state') + "&response_type=code"

def save_access_token(code):
  a = 1

def get_auth_url():
  return authorization_url

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  if underscore_name == "connect_spotify":
    return send_message(authorization_url)
