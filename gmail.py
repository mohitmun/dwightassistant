def get_bot():
  return {"name":'Dwight',
        "description":'An Assistant to you',
        "intents":[
            {
                'intentName': 'GetLastEmailGmail',
                'intentVersion': '$LATEST'
            },
        ],
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
        "childDirected":True}
def get_slots():
  return [
    {
      'name': "From"
    }
  ]
def get_intents():
  return [
    {
      "name": "GetLastEmailGmail",
      "description": "Get last email from you gmail inbox",
      "sampleUtterances": ["Show me last email", "Get me last email", "whats my last email"],
      # "dialogCodeHook": {
      #   "uri": "test",
      #   "messageVersion": "$LATEST"
      # }
      "fulfillmentActivity": {
        "type": "CodeHook",
        "codeHook": {
          "uri": "arn:aws:lambda:us-east-1:420758276632:function:test",
          "messageVersion": "1.0"
        }
      },
      "conclusionStatement": {
        "messages": [
          {
            "contentType": "PlainText",
            "content": "conclu 1"
          },
          {
            "contentType": "PlainText",
            "content": "conclu 2"
          }
        ]
      }
    }
  ]
  