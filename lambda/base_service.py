import utils
import dynamodb
import os
import json
import dotmap
class BaseService:
  
  def __init__(self, service1):
    self.service = service1

  def redirect_to_auth(self, event, authorization_url):
    user_id = event["queryStringParameters"]["user_id"]
    return {
      'statusCode': '302',
      'headers': {
          'Location': authorization_url,
          'Set-Cookie': 'user_id='+ user_id
      },
    }

  def handle(self, event):
    user = dynamodb.get_user(event["userId"])
    if len(user) == 0:
      user = dynamodb.add_user(event["userId"])
      return user
    return user[-1]

  def access_token_key(self):
    return self.service + "_access_token"

  def auth_key(self):
    return self.service + "_auth"

  def get_access_token(self, user):
    if self.access_token_key() in user:
      return user[self.access_token_key()]["S"]
    return None

  def get_and_save_access_code(self, user_id, command):
    response = os.popen(command).read()
    # response = json.loads(response)
    print(response)
    dynamodb.update_user(user_id, self.auth_key(), response)
    response = json.loads(response)
    dynamodb.update_user(user_id, self.access_token_key(), response["access_token"])
    return response

  def send_api_auth_link(self, user_id):
    return utils.send_message("Please give access to you {0} account {1}?user_id={2}".format(self.service, utils.get_api_auth_url("connect-{0}".format(self.service)), user_id))

  def authorized_curl(self, s, user):
    return self.curl("{0} -H 'Authorization: Bearer {1}'".format(s, self.get_access_token(user)))

  def curl(self, s):
    cmd = "curl {0}".format(s)
    print(cmd)
    res = os.popen(cmd).read()
    res = json.loads(res)
    res = dotmap.DotMap(res)
    return res