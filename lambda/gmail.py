# event_method_mapping = {"Get"}
from requests_oauth2 import OAuth2
import os
import utils
import dynamodb
import json
from urllib import quote, urlencode
import base64
import base_service
import base64
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
    'statusCode': '200',
    'body': json.dumps({"message": "Gmail Connected, Now you can go back to chatbot!"}),
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
  user = base_service.get_and_save_access_code(base_service.get_user_id(user), command)
  return user

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  user = base_service.handle(event)
  access_token = base_service.get_access_token(user)
  if access_token != None:
    if base_service.token_expired(user):
      user = refresh_access_token(user)
    if underscore_name == "get_email_gmail":
      return get_email_gmail(user, event)
    if underscore_name == "delete_mail_gmail":
      return delete_mail_gmail(user)
    if underscore_name == "send_mail_gmail":
      return send_mail_gmail(user, event)
  else:
    return base_service.send_api_auth_link(base_service.get_user_id(user))

def token_expired(user):
  return base_service.token_expired(user)

def search_gmail(user, event):
  return utils.send_message("searching gmail event:" + json.dumps(event))

def delete_mail_gmail(user):
  if "last_mail_id" in user:
    base_service.authorized_curl("https://www.googleapis.com/gmail/v1/users/me/messages/{}/trash".format(user["last_mail_id"]["S"]), user)
    return utils.send_message("Following mail has been trashed\n" + format_gmail_message(get_message(user["last_mail_id"]["S"])))
  else:
    return utils.send_message("No mail present to delete")

def send_mail_gmail(user, event):
  slots = event["currentIntent"]["slots"]
  reply = slots["reply_intent_slot"]
  email_message_slot = slots["email_message_slot"]
  subject_slot = slots["subject_slot"]
  email_slot = slots["email_slot"]
  sessionAttributes = event["sessionAttributes"]
  if sessionAttributes == None:
    sessionAttributes = {}
  else:
    if "email_slot" in sessionAttributes and sessionAttributes["email_slot"] == "not_done":
      email_slot = event['inputTranscript']
      slots["email_slot"] = email_slot
      sessionAttributes["email_slot"] = email_slot
    if "email_message_slot" in sessionAttributes and sessionAttributes["email_message_slot"] == "not_done":
      email_message_slot = event['inputTranscript']
      slots["email_message_slot"] = email_message_slot
      sessionAttributes["email_message_slot"] = email_message_slot
    if "subject_slot" in sessionAttributes and sessionAttributes["subject_slot"] == "not_done":
      subject_slot = event['inputTranscript']
      slots["subject_slot"] = subject_slot
      sessionAttributes["email_message_slot"] = subject_slot
  if email_slot == None:
    sessionAttributes["email_slot"] = "not_done"
    return elicit_slot(slots, "email_slot", sessionAttributes)
  if email_message_slot == None:
    sessionAttributes["email_message_slot"] = "not_done"
    return elicit_slot(slots, "email_message_slot", sessionAttributes)
  if reply != None:
    last_mail_id = user["last_mail_id"]["S"]
    if last_mail_id:
      return send_email(user, message_id=last_mail_id, body=email_message_slot)
    else:
      return utils.send_message("No message found to delete")
  if subject_slot == None:
    sessionAttributes["subject_slot"] = "not_done"
    return elicit_slot(slots, "subject_slot", sessionAttributes)
  return send_email(user, subject= subject_slot, to_email= email_slot, body= email_message_slot)

def elicit_slot(slots, slot, session):
  return {"dialogAction": {
    "type": "ElicitSlot",
    "intentName": "SendMailGmail",
    "slots": slots,
    "slotToElicit" : slot
    },
    'sessionAttributes': session
  }
def send_email(user,**args):
  reply = False
  if "message_id" in args:
    reply = True
    message = get_message(args["message_id"], user)
    args["to_email"] = get_from(message)
    args["subject"] = "Re: " + get_subject(message)
  draft_message = "To: "+args["to_email"]+"\r\n" +    "From: <"+get_user_email(user)+">\r\n" +     "Subject: "+args["subject"]+"\r\n" +    "Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n" +    args["body"]+"\r\n"
  print("=====")
  print(draft_message)
  print("=====")
  encodedMail = base64.b64encode(draft_message).replace("+", "-").replace("//", "_")
  url = "https://www.googleapis.com/gmail/v1/users/me/messages/send"
  res = base_service.authorized_curl("'{}' --data '{}' -H 'Content-Type: application/json'".format(url, json.dumps({"raw":encodedMail}) ), user)
   
  if "id" in res:
    return utils.send_message("{}!\n{}".format("Replied" if reply else "Message sent", format_gmail_message(get_message(res["id"], user))))
  else: 
    return utils.send_message("Email sending failed")

def get_user_email(user):
  auth = json.loads(user["gmail_auth"]["S"])
  payload = auth["id_token"].split(".")[1]
  payload = payload.encode('ascii') 
  padded = payload + '=' * (4 - len(payload) % 4) 
  padded = base64.urlsafe_b64decode(padded)
  res = json.loads(padded)
  return res["email"]

def get_search_query(args):
  q = args.pop("q", "")
  res = ""
  for key in args:
    value = args[key]
    if value:
      res = res + key + ":" + value + " "
  # is From To Subject after: before: yyyy/mm/dd
  if q != None:
    res = res + q
  return res

# event = {"currentIntent": {"slots": {"email_type_slot": "", "query_slot": "", "time_slot": "", "date_slot": "", "from_person_slot": "", "to_person_slot": "", "from_first_name_slot": "", "to_first_name_slot": ""}}}
def get_search_query_from_event(event):
  slots = event["currentIntent"]["slots"]
  amazong_time = slots["time_slot"]
  amazong_date = slots["date_slot"]
  from_ = slots["from_person_slot"]
  to_email = slots["to_person_slot"]
  if from_ == None:
    from_ = slots["from_first_name_slot"]  
  if to_email == None:
    to_email = slots["to_first_name_slot"]  
  search_args = {"is":slots["email_type_slot"], "to": to_email, "from": from_, "q": slots["query_slot"]}   
  q = get_search_query(search_args)
  return q

def get_email_gmail(user, event):
  url = "https://www.googleapis.com/gmail/v1/users/me/messages?maxResults=1"
  q = get_search_query_from_event(event)
  if q:
    url = url + "&q=" + quote(q)
  res = base_service.authorized_curl("'{}'".format(url), user)
  print(res)
  if "messages" in res and len(res["messages"]) > 0:
    message_id = res["messages"][0]["id"]
    message = get_message(message_id, user)
    dynamodb.update_user(base_service.get_user_id(user), "last_mail_id", message_id)
    return utils.send_message(format_gmail_message(message))
  else:
    return utils.send_message("No messages found")
  # return utils.send_card(message.snippet, message.snippet, get_from(message), {"Reply":"Reply", "Archive":"Archive", "Delete": "Delete"})

def format_gmail_message(message):
  result = "To: {}\nFrom: {}\nSubject: {}\nBody: {}\nClick here to view https://mail.google.com/mail/u/0/#inbox/{}".format(get_to(message), get_from(message), get_subject(message), get_body(message), message["id"])
  return result


def get_message(message_id, user):
  url = "https://www.googleapis.com/gmail/v1/users/me/messages/{0}?format=metadata".format(message_id)
  res = base_service.authorized_curl(url, user)
  return res

def get_body(message):
  #todo see why snippet is not proper
  return message["snippet"]

def get_to(message):
  h = message["payload"]["headers"]
  return [a for a in h if a['name'] == "To"][0]["value"]

def get_from(message):
  h = message["payload"]["headers"]
  return [a for a in h if a['name'] == "From"][0]["value"]

def get_subject(message):
  h = message["payload"]["headers"]
  return [a for a in h if a['name'] == "Subject"][0]["value"]

# DotMap(internalDate=u'1500214393000', historyId=u'11074', payload=DotMap(mimeType=u'multipart/mixed', headers=[DotMap(name=u'Received', value=u'from 816660975287 named unknown by gmailapi.google.com with HTTPREST; Sun, 16 Jul 2017 07:13:13 -0700'), DotMap(name=u'Date', value=u'Sun, 16 Jul 2017 07:13:13 -0700'), DotMap(name=u'From', value=u'Testmohitpara <testmohitpara@gmail.com>'), DotMap(name=u'To', value=u'testmohitpara@gmail.com'), DotMap(name=u'Message-Id', value=u'<CAKLm4q97Q=8AN=J+KX5kN2HP4dmzKS2Dzhz0LGKKgpuGx1kS-w@mail.gmail.com>'), DotMap(name=u'Subject', value=u'To: ravi@actonmagic.com new'), DotMap(name=u'Mime-Version', value=u'1.0'), DotMap(name=u'Content-Type', value=u'multipart/mixed; boundary="--==_mimepart_596b7471ccd32_131a43ff155c101d464970"; charset=UTF-8'), DotMap(name=u'Content-Transfer-Encoding', value=u'7bit')]), snippet=u'new', sizeEstimate=878, threadId=u'15d4bbef83ebb537', labelIds=[u'SENT', u'INBOX'], id=u'15d4bbef83ebb537')
def test_user():
  return dynamodb.get_item("QC9PVI")

def test():
  return get_email_gmail(test_user())