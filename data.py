import yaml
def get_bot():
  intents = []
  for i in get_intents():
    intents.append(
            {
                'intentName': i["name"],
                'intentVersion': '$LATEST'
            })
  return {"name":'Dwight',
        "description":'An Assistant to you',
        "intents": intents,
        "clarificationPrompt":{
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Welcome to Dwight. Type "Show me my last email"'
                },
            ],
            'maxAttempts': 5,
            'responseCard': 'string'
        },
        "abortStatement":{
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Bot failed'
                },
            ],
            'responseCard': 'string'
        },
        "idleSessionTTLInSeconds":123,
        "locale":'en-US',
        "childDirected":True,
        }
def get_slots():
  return [
    {
      'name': "From"
    }
  ]
def get_intents():
  with open("data.yml", 'r') as stream:
    try:
        return yaml.load(stream)["intents"]
    except yaml.YAMLError as exc:
        print(exc)