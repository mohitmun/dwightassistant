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

    if event["resource"] == "/gmail":
      return gmail.save_access_token(event)
    if event["resource"] == "/connect-gmail":
      return gmail.redirect_to_auth(event)

def test():
  event = {
  "currentIntent": {
    "slots": {},
    "name": "PlaySpotify",
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
  "resource": "/spotify",
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
  "queryStringParameters": {"code": "AQB71S_brJ0i-HbiFiJr4N5RMCtTcU1fGo-YqUQapJ9WuPDyxI-ICHZtOzOTDlEre1zWjkOrmgrSuoAYp4SSKZGUAlQ7o3Za8F56X4OddiqFvAyg-SswbUYdJIZ66QXZvEpU3pflUXmI3NHB-w84qs_IynPTw0eWwJ8B3PlDJDkImGXk10LyA5ckvX6-n6Po_Hxj2-k8Qx_dx0Eepf2MHeEMMuvsCoMCYf2CtsVEzISqUf-VvsosnrqMA2ZCMAbMHECTzl7bLucsBUAiJGtaN53n2kYL2BA-dQem0ezLqw9lBHY3scSWNxgUbOuyeL1d2M6UkPpt7F8t13oLn4Ds9lIXcMRw86KMwoh9FI5gFeJji3drcCP1u2ylFAlr27oKRstyouejaDNEpY372tuEpJgBuw-tS7FjZYVbR-Sr--5NqkljhrecMjQYHTP6BzQWKKMA4lSM65SS_xYRV7ASmSoAB-qfyIKc_pgGGjD5qpWUBX239g88MFBvQIk6hdfM_XDgXSEE3eMb749vUoUN6nMo7VyPu7nnciNZwJoT1ZTVPK6E9zfJGsVsGGDwyiHnlXBjlwTUEtonn7xy9mt7L09HWn8Lt0UjHME_JYJA1hpI8z21O-Sz7pQdHh1JdB2QFMOB1fW9v7o0mLORepDcFVjGpNXkEfXCbw4mXEpYZLGc6omgvrSXmhCpbJebNBDyXpi8Fyywi7WP6UKLbD_M", "user_id": "123"},
  "httpMethod": "GET",
  "pathParameters": "null",
  # "headers": "null",
  "headers": {
   "Cookie": "user_id=ZAKQI3"
  },
  "stageVariables": "null",
  "path": "/spotify",
  "isBase64Encoded": "false"
}
  return lambda_handler(event, {})