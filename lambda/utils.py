import re
import json
import os
def convert_camelcase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_api_auth_url(end_point):
  return "https://tn78yzlfic.execute-api.us-east-1.amazonaws.com/a/" + end_point

def get_latlong(s):
  command = "curl 'https://maps.googleapis.com/maps/api/geocode/json?address={0}'".format(s.replace(" ", "+"))
  res = os.popen(command).read()
  res = json.loads(res)
  res = res["results"][0]["geometry"]["location"]
  return res

def send_card(message, title, subTitle, buttons_dict):
  buttons = []
  for keyvalue in buttons_dict:
    for key in keyvalue:
      buttons = buttons + [{"text": key, "value": keyvalue[key]}]
  return {
      "sessionAttributes": {},
      "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message": {
          "contentType": "PlainText",
          "content": message
        }
        ,
       "responseCard": {
          
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": [
              {
                 "title":title,
                 "subTitle":subTitle,
                 # "imageUrl":imageUrl,
                 # "attachmentLinkUrl":attachmentLinkUrl,
                 "buttons":buttons
               } 
           ] 
         }
      }
    }

def send_message(message):
  if type(message) is dict:
    message = "Dict: "+ json.dumps(message)
  if type(message) is list:
    message = "List: " + json.dumps(message)
  return {
    "sessionAttributes": {},
    "dialogAction": {
      "type": "Close",
      "fulfillmentState": "Fulfilled",
      "message": {
        "contentType": "PlainText",
        "content": message
      }
    }
  }
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