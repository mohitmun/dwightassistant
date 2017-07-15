import json
import gmail
import utils
def lambda_handler(event, context):
    currentIntent = event["currentIntent"]["name"]
    service = utils.convert_camelcase(currentIntent).split("_")[-1]
    if service == "gmail":
      return gmail.handle(event)
    return "no service found"
    # TODO implement
    # return {
    #   "sessionAttributes": {},
    #   "dialogAction": {
    #     "type": "Close",
    #     "fulfillmentState": "Fulfilled",
    #     "message": {
    #       "contentType": "PlainText",
    #       "content": "hello bro" + json.dumps(event)
    #     }
       #  ,
       # "responseCard": {
       #    "version": integer-value,
       #    "contentType": "application/vnd.amazonaws.card.generic",
       #    "genericAttachments": [
       #        {
       #           "title":"card-title",
       #           "subTitle":"card-sub-title",
       #           "imageUrl":"URL of the image to be shown",
       #           "attachmentLinkUrl":"URL of the attachment to be associated with the card",
       #           "buttons":[ 
       #               {
       #                  "text":"button-text",
       #                  "value":"Value sent to server on button click"
       #               }
       #            ]
       #         } 
       #     ] 
       #   }
      # }
    # }
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