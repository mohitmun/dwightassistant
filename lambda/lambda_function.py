import json
import gmail
import spotify
import utils
def lambda_handler(event, context):
  currentIntent = event["currentIntent"]["name"]
  service = utils.convert_camelcase(currentIntent).split("_")[-1]
  if service == "gmail":
    return gmail.handle(event)
  if service == "spotify":
    return spotify.handle(event)
  #check if oauth2
  if event["resource"] == "/spotify":
    code = event["queryStringParameters"]["code"]
    spotify.save_access_token(code)

def test():
  event = {
  "currentIntent": {
    "slots": {},
    "name": "ConnectSpotify",
    "confirmationStatus": "None"
  },
  "bot": {
    "alias": "null",
    "version": "$LATEST",
    "name": "Dwight"
  },
  "userId": "yf3gelerh094t4w42kqqtcc7d9oejbhv",
  "inputTranscript": "show me my last mail",
  "invocationSource": "FulfillmentCodeHook",
  "outputDialogMode": "Text",
  "messageVersion": "1.0",
  "sessionAttributes": {}
  }
  return lambda_handler(event, {})