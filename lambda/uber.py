# event_method_mapping = {"Get"}
from requests_oauth2 import OAuth2
import os
import utils
import dynamodb
import json
from urllib import quote, urlencode
import base64
import base_service
service = "uber"
base_service = base_service.BaseService(service)
redirect_uri = utils.get_api_auth_url(service)
client_id = os.environ['UBER_CLIENT_ID']
client_secret = os.environ['UBER_CLIENT_SECRET']
auth_base = "https://login.uber.com/oauth/v2/"
oauth2_handler = OAuth2(client_id, client_secret, auth_base, redirect_uri, "authorize", "token")
authorization_url = oauth2_handler.authorize_url('request profile history all_trips') + "&response_type=code"

def get_and_save_access_code(code, user_id):
  command = "curl https://login.uber.com/oauth/v2/token -F 'code={0}' -F 'client_id={1}' -F 'client_secret={2}' -F 'redirect_uri={3}' -F 'grant_type=authorization_code'".format(code, client_id, client_secret, redirect_uri)
  print(command)
  return base_service.get_and_save_access_code(user_id, command)

def save_access_token(event):
  code = event["queryStringParameters"]["code"]
  user_id = event["headers"]["Cookie"].split("=")[-1]
  res = get_and_save_access_code(code, user_id)
  return {
    #todo remove res
    'statusCode': '200',
    'body': json.dumps({"message": "Uber Connected!",  "event": event, "res": res}),
    'headers': {
        'Content-Type': 'application/json',
    },
  }

def redirect_to_auth(event):
  return base_service.redirect_to_auth(event, authorization_url)

def get_authorization_url():
  return authorization_url

def refresh_access_token(user):
  command = "curl https://login.uber.com/oauth/v2/token -F 'refresh_token={0}' -F 'client_id={1}' -F 'client_secret={2}' -F 'grant_type=refresh_token'".format(base_service.get_refresh_token(user), client_id, client_secret)
  print("refresing token")
  res = os.popen(command).read()
  print(command)
  print(res)
  base_service.save_credentials(base_service.get_user_id(user), res)
  return res

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  user = base_service.handle(event)
  access_token = base_service.get_access_token(user)
  if access_token != None:
    if base_service.token_expired(user):
      refresh_access_token(user)
    if underscore_name == "get_last_email_gmail":
      return get_last_email_gmail(user)
  else:
    return base_service.send_api_auth_link(base_service.get_user_id(user))

def token_expired(user):
  return base_service.token_expired(user)
