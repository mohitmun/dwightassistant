import boto3
import string
import random
import os
client = boto3.client('dynamodb')

TableName = os.environ["BOT_NAME"]
def add_user(lex_user_id):
  random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
  res = client.put_item(TableName=TableName, Item={"user_id": {"S": random_id}, "lex_user_id": {"S": lex_user_id}})
  return get_item(random_id)

def get_item(id):
  return client.get_item(TableName=TableName, Key={"user_id": {"S": id}})["Item"]

def update_user(user_id, key, value):
  return client.update_item(TableName=TableName, Key={"user_id":{"S":user_id}}, AttributeUpdates={key:{"Value":{"S":value}}})

def get_user(lex_user_id):
  return client.scan(TableName=TableName, FilterExpression="lex_user_id = :a", ExpressionAttributeValues={
        ':a': {
            'S': lex_user_id,
        }})["Items"]