import boto3

class LexApi:
  
  def __init__(self):
    self.client = boto3.client('lex-models')
  def create_dwight(self):
    response = self.client.put_bot(
      name='Dwight',
      description='An Assistant to you',
      # intents=[
      #     {
      #         'intentName': 'getLastEmail',
      #         'intentVersion': '$LATEST'
      #     },
      # ],
      clarificationPrompt={
          'messages': [
              {
                  'contentType': 'PlainText',
                  'content': 'Welcome to Dwight. Type "Show me my last email"'
              },
          ],
          'maxAttempts': 5,
          'responseCard': 'string'
      },
      abortStatement={
          'messages': [
              {
                  'contentType': 'PlainText',
                  'content': 'Bot failed'
              },
          ],
          'responseCard': 'string'
      },
      idleSessionTTLInSeconds=123,
      locale='en-US',
      childDirected=True|False
    )
  def create_intent(self):
    response = self.client.put_intent(
      name="GetLastMail"
    )