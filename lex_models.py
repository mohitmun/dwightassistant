import boto3
import gmail
class LexApi:
  def __init__(self):
    self.client = boto3.client('lex-models')
  def delete_bot(self):
    response = self.client.delete_bot(name="Dwight")
    return response
  def delete_intent(self, name):
    response = self.client.delete_intent(name=name)
    return response
  def create_bot(self):
    response = self.client.put_bot(**gmail.get_bot())
    return response
  def create_intent(self):
    res = []
    for intent in gmail.get_intents():
      response = self.client.put_intent(**intent)
      res.append(response)
    return res
  def get_bots(self):
    return self.client.get_bots()
  # def set_up_bot():
  #   pass

class LexRunTimeApi:
  """docstring for LexRunTimeApi"""
  def __init__(self):
    self.client = boto3.client('lex-runtime')
  def send_message(self, message):
#     client.post_text(
#     botName='string',
#     botAlias='string',
#     userId='string',
#     sessionAttributes={
#         'string': 'string'
#     },
#     inputText='string'
# )
    return self.client.post_text(botName="Dwight", botAlias="$LATEST", userId="mama", inputText=message)