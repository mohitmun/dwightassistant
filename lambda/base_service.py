import utils
import dynamodb

def redirect_to_auth(event, authorization_url):
  user_id = event["queryStringParameters"]["user_id"]
  return {
    'statusCode': '302',
    'headers': {
        'Location': authorization_url,
        'Set-Cookie': 'user_id='+ user_id
    },
  }

def handle(event, service):
  user = dynamodb.get_user(event["userId"])
  if len(user) == 0:
    user = dynamodb.add_user(event["userId"])
  return user[-1]

def send_api_auth_link(service, user_id):
  return utils.send_message("Please give access to you {0} account {1}?user_id={2}".format(service, utils.get_api_auth_url("connect-{0}".format(service)), user_id))