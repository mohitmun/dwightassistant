import re
import json
import os
def convert_camelcase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_api_auth_url(end_point):
  return os.environ['OAUTH_APIGATEWAY_URL'] + end_point

def get_latlng(s):
  command = "curl 'https://maps.googleapis.com/maps/api/geocode/json?address={0}'".format(s.replace(" ", "+"))
  res = os.popen(command).read()
  res = json.loads(res)
  res = res["results"][0]["geometry"]["location"]
  return res
# slack
# <div id="special_formatting_text" class="special_formatting_tips showing" aria-hidden="true"><b>*bold*</b> <i>_italics_</i> ~strike~ <code>`code`</code> <code class="preformatted">```preformatted```</code> <span class="quote">&gt;quote</span></div>
def send_card(message, title, subTitle, buttons_dict):
  buttons = []
  for key in buttons_dict:
    buttons = buttons + [{"text": key, "value": buttons_dict[key]}]
  result = {
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
  #todo
  # a = result["dialogAction"].pop("responseCard", None)
  print("seinding card")
  print(result)
  return result

def send_message(message):
  if type(message) is dict:
    message = "Dict: "+ json.dumps(message)
  if type(message) is list:
    message = "List: " + json.dumps(message)
  result = {
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
  print("sending message")
  print(result)
  return result
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