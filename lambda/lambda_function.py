import json
import gmail
import spotify
import utils
def lambda_handler(event, context):
  if "currentIntent" in event:
    currentIntent = event["currentIntent"]["name"]
    service = utils.convert_camelcase(currentIntent).split("_")[-1]
    if service == "gmail":
      return gmail.handle(event)
    if service == "spotify":
      return spotify.handle(event)
  elif "resource" in event:
    if event["resource"] == "/spotify":
      return spotify.save_access_token(event)
    if event["resource"] == "/connect-spotify":
      return spotify.redirect_to_auth(event)


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

def test_spo():
  event = {
  "body": "null",
  "resource": "/connect-spotify",
  "requestContext": {
    "resourceId": "r1iee2",
    "apiId": "tn78yzlfic",
    "resourcePath": "/spotify",
    "httpMethod": "GET",
    "requestId": "test-invoke-request",
    "path": "/spotify",
    "accountId": "420758276632",
    "identity": {
      "apiKey": "test-invoke-api-key",
      "userArn": "arn:aws:iam::420758276632:root",
      "cognitoAuthenticationType": "null",
      "accessKey": "ASIAJVPJCQXOC6JWQKVQ",
      "caller": "420758276632",
      "userAgent": "Apache-HttpClient/4.5.x (Java/1.8.0_112)",
      "user": "420758276632",
      "cognitoIdentityPoolId": "null",
      "cognitoIdentityId": "null",
      "cognitoAuthenticationProvider": "null",
      "sourceIp": "test-invoke-source-ip",
      "accountId": "420758276632"
    },
    "stage": "test-invoke-stage"
  },
  "queryStringParameters": {"code": "chus", "user_id": "123"},
  "httpMethod": "GET",
  "pathParameters": "null",
  "headers": "null",
  "stageVariables": "null",
  "path": "/spotify",
  "isBase64Encoded": "false"
}
  return lambda_handler(event, {})