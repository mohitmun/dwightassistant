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
base_service = base_service.BaseService(service)
redirect_uri = utils.get_api_auth_url(service)
client_id = os.environ['GMAIL_CLIENT_ID']
client_secret = os.environ['GMAIL_CLIENT_SECRET']
auth_base = "https://accounts.google.com/o/oauth2/"
oauth2_handler = OAuth2(client_id, client_secret, auth_base, redirect_uri, "auth", "token")
authorization_url = oauth2_handler.authorize_url('email https://www.googleapis.com/auth/gmail.modify') + "&response_type=code&access_type=offline&prompt=consent"

def get_and_save_access_code(code, user_id):
  command = "curl https://www.googleapis.com/oauth2/v4/token -d 'code={0}' -d 'client_id={1}' -d 'client_secret={2}' -d 'redirect_uri={3}' -d 'grant_type=authorization_code'".format(code, client_id, client_secret, redirect_uri)
  print(command)
  return base_service.get_and_save_access_code(user_id, command)

def save_access_token(event):
  code = event["queryStringParameters"]["code"]
  user_id = event["headers"]["Cookie"].split("=")[-1]
  res = get_and_save_access_code(code, user_id)
  return {
    #todo remove res
    'statusCode': '200',
    'body': json.dumps({"message": "Gmail Connected!",  "event": event, "res": res}),
    'headers': {
        'Content-Type': 'application/json',
    },
  }

def redirect_to_auth(event):
  return base_service.redirect_to_auth(event, authorization_url)

def get_authorization_url():
  return authorization_url

def refresh_access_token(user):
  print("refresing token")
  command = "curl https://www.googleapis.com/oauth2/v4/token -d 'refresh_token={0}' -d 'client_id={1}' -d 'client_secret={2}' -d 'grant_type=refresh_token'".format(base_service.get_refresh_token(user), client_id, client_secret)
  print(command)
  res = os.popen(command).read()
  res = json.loads(res)
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

def get_last_email_gmail(user):
  res = base_service.authorized_curl("https://www.googleapis.com/gmail/v1/users/me/messages?maxResults=1", user)
  print(res)
  message = get_message(res.messages[0].id, user)
  return utils.send_card(message.snippet, message.snippet, get_from(message), [{"Reply":"Reply"}, {"Archive":"Archive"}, {"Forward": "Forward"}, {"Delete": "Delete"}])

def get_message(message_id, user):
  url = "https://www.googleapis.com/gmail/v1/users/me/messages/{0}?format=metadata".format(message_id)
  res = base_service.authorized_curl(url, user)
  return res

def search_by_content(content, user):
  return []

def get_to(message):
  h = message.payload.headers
  return [a for a in h if a['name'] == "To"][0].value

def get_from(message):
  h = message.payload.headers
  return [a for a in h if a['name'] == "From"][0].value

def get_subject(message):
  h = message.payload.headers
  return [a for a in h if a['name'] == "Subject"][0].value

# DotMap(internalDate=u'1500214393000', historyId=u'11074', payload=DotMap(mimeType=u'multipart/mixed', headers=[DotMap(name=u'Received', value=u'from 816660975287 named unknown by gmailapi.google.com with HTTPREST; Sun, 16 Jul 2017 07:13:13 -0700'), DotMap(name=u'Date', value=u'Sun, 16 Jul 2017 07:13:13 -0700'), DotMap(name=u'From', value=u'Testmohitpara <testmohitpara@gmail.com>'), DotMap(name=u'To', value=u'testmohitpara@gmail.com'), DotMap(name=u'Message-Id', value=u'<CAKLm4q97Q=8AN=J+KX5kN2HP4dmzKS2Dzhz0LGKKgpuGx1kS-w@mail.gmail.com>'), DotMap(name=u'Subject', value=u'To: ravi@actonmagic.com new'), DotMap(name=u'Mime-Version', value=u'1.0'), DotMap(name=u'Content-Type', value=u'multipart/mixed; boundary="--==_mimepart_596b7471ccd32_131a43ff155c101d464970"; charset=UTF-8'), DotMap(name=u'Content-Transfer-Encoding', value=u'7bit')]), snippet=u'new', sizeEstimate=878, threadId=u'15d4bbef83ebb537', labelIds=[u'SENT', u'INBOX'], id=u'15d4bbef83ebb537')
def test():
  user = dynamodb.get_item("AE66R0")
  return get_last_email_gmail(user)