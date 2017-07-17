from requests_oauth2 import OAuth2
import os
import utils
import dynamodb
import json
from urllib import quote, urlencode
import base64
import base_service
service = "spotify"
redirect_uri = utils.get_api_auth_url("spotify")
oauth2_handler = OAuth2(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'], "https://accounts.spotify.com/", redirect_uri, "authorize", "api/token")
authorization_url = oauth2_handler.authorize_url('user-read-playback-state playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-follow-read user-follow-modify user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state') + "&response_type=code"

def save_access_token(event):
  code = event["queryStringParameters"]["code"]
  user_id = event["headers"]["Cookie"].split("=")[-1]
  res = get_and_save_access_code(code, user_id)
  return {
    'statusCode': '200',
    'body': json.dumps({"message": "Spotify Connected!",  "event": event, "res": res}),
    'headers': {
        'Content-Type': 'application/json',
    },
  }

def get_and_save_access_code(code, user_id):
  base64_id_secret = base64.b64encode("{0}:{1}".format(os.environ["SPOTIFY_CLIENT_ID"], os.environ["SPOTIFY_CLIENT_SECRET"]))
  command = "curl -d grant_type=authorization_code -d code={0} -d redirect_uri={1} -H \"Authorization: Basic {2}\" \"https://accounts.spotify.com/api/token\"".format(code, quote(redirect_uri), base64_id_secret, 'utf-8')
  print(command)
  response = os.popen(command).read()
  # response = json.loads(response)
  dynamodb.update_user(user_id, "spotify_auth", response)
  response = json.loads(response)
  dynamodb.update_user(user_id, "spotify_access_token", response["access_token"])
  return response

def redirect_to_auth(event):
  return base_service.redirect_to_auth(event, authorization_url)

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  user = base_service.handle(event, service)
  if underscore_name == "play_spotify":
    return play_spotify(user)
  if underscore_name == "stop_spotify":
    return stop_spotify(user)

def play_spotify(user):
  command = "curl -X PUT 'https://api.spotify.com/v1/me/player/play' -H 'Authorization: Bearer {0}'".format(user["spotify_access_token"]["S"])
  return utils.send_message(os.popen(command).read())

def stop_spotify(user):
  command = "curl -X PUT 'https://api.spotify.com/v1/me/player/pause' -H 'Authorization: Bearer {0}'".format(user["spotify_access_token"]["S"])
  return utils.send_message(os.popen(command).read())
# curl -X PUT "https://api.spotify.com/v1/me/player/play" -H "Authorization: Bearer BQCF5bnU0EY0uTpkoC3HUl-66YJjZXu5ULt503BHEP-9WkMcro2xJcO4atyxl04hIdW4z_aLdHwslDX40oJSAsmX2h6e99Dvv4EOAl7Xj4dM_utbPJf9Adk0fuD0yas_vfPTjpjgfdmQYkE"

# https://accounts.spotify.com/authorize/?client_id=a7ed7ac582c4421397e4336a9339d849&response_type=code&redirect_uri=https%3A%2F%2Fmamam.com&scope=user-modify-playback-state




# \curl -d grant_type=authorization_code -d code=AQBpjD88SGOBw7k5G1C64tC-6qEZnwSSQl56t-9EPKZ58ZvaD4xdY9GO_xQbHBM5M0bEuKFqCkNlFtlTOf_NQFVi1K_YhAWuL_xKTRcmN3Oym62qFv-f-JTL2IRFkH6b0eFMuigb9X-toElrDV3gBLTAlX8UNkoo4voGNPxJAAOlp_nulVJh-gJkNWG4Qvjvp3tGxg6pA7_kd5UrLxB6G5_W2w -d redirect_uri=https%3A%2F%2Fmamam.com -H "Authorization: Basic YTdlZDdhYzU4MmM0NDIxMzk3ZTQzMzZhOTMzOWQ4NDk6NmRkNTQ4MGY2NzNkNGZlZThmN2QyMjU3MzdhOWViN2E=" "https://accounts.spotify.com/api/token"


# {"access_token":"BQCF5bnU0EY0uTpkoC3HUl-66YJjZXu5ULt503BHEP-9WkMcro2xJcO4atyxl04hIdW4z_aLdHwslDX40oJSAsmX2h6e99Dvv4EOAl7Xj4dM_utbPJf9Adk0fuD0yas_vfPTjpjgfdmQYkE","token_type":"Bearer","expires_in":3600,"refresh_token":"AQAWdn2eyEmmM8e1-QpSkrQjcrCoA7YS2srYsV_G5enD6CSazPm8kDRi8hYrbmrqQjG8cO_QvcxM0THV2leLEpcOKGFzdc37zjSLzbJ0MFS0IjGZZakk99yvrdfScTwE1hA","scope":"user-modify-playback-state"}