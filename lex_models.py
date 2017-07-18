import boto3
import data
import os
class LexApi:
  def __init__(self):
    self.client = boto3.client('lex-models')
  def delete_bot(self):
    response = self.client.delete_bot(name="Dwight")
    return response
  def delete_intent(self):
    self.delete_bot();
    for intent in data.get_intents():    
      response = self.client.delete_intent(name=intent['name'])
    return True
  def create_bot(self):
    params = data.get_bot()
    try:
      params["checksum"] = self.get_bot(params["name"])["checksum"]
    except Exception as e:
      pass
    response = self.client.put_bot(**params)
    return response
  def create_intents(self):
    res = []
    for intent in data.get_intents():
      try:        
        intent["checksum"] = self.get_intent(intent["name"])["checksum"]
      except Exception as e:
        pass        
      response = self.client.put_intent(**intent)
      res.append(response)
    return res
  def create_slot_types(self):
    print("chus")
    res = []
    for slot_type in data.get_slot_types():
      try:        
        slot_type["checksum"] = self.get_slot_type(slot_type["name"])["checksum"]
      except Exception as e:
        pass        
      response = self.client.put_slot_type(**slot_type)
      res.append(response)
    return res
  def get_bots(self):
    return self.client.get_bots()
  # def set_up_bot():
  #   pass
  def get_bot(self, name):
    return self.client.get_bot(name=name,versionOrAlias="$LATEST")
  def get_bot_channel_associations(self):
    return self.client.get_bot_channel_associations(botName="Dwight",botAlias="LATEST")
  def get_intent(self, name):
    return self.client.get_intent(name=name, version="$LATEST")
  def get_slot_type(self, name):
    return self.client.get_slot_type(name=name, version="$LATEST")

class LexRunTimeApi:
  """docstring for LexRunTimeApi"""
  def __init__(self):
    self.client = boto3.client('lex-runtime')
  def send_message(self, userId, message):
#     client.post_text(
#     botName='string',
#     botAlias='string',
#     userId='string',
#     sessionAttributes={
#         'string': 'string'
#     },
#     inputText='string'
# )
    return self.client.post_text(botName=os.environ["BOT_NAME"], botAlias="$LATEST", userId=userId, inputText=message)