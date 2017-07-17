# event_method_mapping = {"Get"}
from requests_oauth2 import OAuth2
import os
import utils
import dynamodb
import json
from urllib import quote, urlencode
import base64
import base_service
service = "gmail"
redirect_uri = utils.get_api_auth_url(service)
oauth2_handler = OAuth2(os.environ['GMAIL_CLIENT_ID'], os.environ['GMAIL_CLIENT_SECRET'], "https://accounts.spotify.com/", redirect_uri, "authorize", "api/token")
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
  if "spotify_access_token" in user:
    if underscore_name == "get_last_email_gmail":
      return get_last_email()
  else:
    return base_service.send_api_auth_link(service, user["user_id"]["S"])

def get_last_email():
  message = "this is last mail"
  return utils.send_message(message)