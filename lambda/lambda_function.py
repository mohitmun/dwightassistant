import json
import gmail
import utils
def lambda_handler(event, context):
  currentIntent = event["currentIntent"]["name"]
  service = utils.convert_camelcase(currentIntent).split("_")[-1]
  if service == "gmail":
    return gmail.handle(event)
  return "no service found"
  
def test():
  event = {
  "currentIntent": {
    "slots": {},
    "name": "GetLastEmailGmail",
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