import json
def lambda_handler(event, context):
    # TODO implement
    return {
      "sessionAttributes": {},
      "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": "chus mamamamam" + json.dumps(event)
        }
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
      }
    }