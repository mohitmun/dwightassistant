import yaml
import os
def get_bot():
  intents = []
  for i in get_intents():
    intents.append({
      'intentName': i["name"],
      'intentVersion': '$LATEST'
    })
  with open("data.yml", 'r') as stream:
    result = yaml.load(stream)["bot"]
  result["intents"] = intents
  return result

def get_intents():
  with open("data.yml", 'r') as stream:
    items = yaml.load(stream)["intents"]
    for item in items:
      item["fulfillmentActivity"] = {
      "type": "CodeHook",
      "codeHook": {
  
        "messageVersion": "1.0",
        "uri": os.environ["LAMBDA_URI"]
      }
    }
    return items

def get_slot_types():
  with open("data.yml", 'r') as stream:
    return yaml.load(stream)["slot_types"]
    