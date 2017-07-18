import yaml
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
    return yaml.load(stream)["intents"]

def get_slot_types():
  with open("data.yml", 'r') as stream:
    return yaml.load(stream)["slot_types"]
    