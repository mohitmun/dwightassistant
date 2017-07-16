import boto3
import string
import random
client = boto3.client('dynamodb')

def add_user(lex_user_id):
  random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
  client.put_item(TableName="users", Item={"user_id": {"S": random_id}, "lex_user_id": {"S": lex_user_id}})
  return random_id

def update_user(user_id, key, value):
  return client.update_item(TableName="users", Key={"user_id":{"S":user_id}}, AttributeUpdates={key:{"Value":{"S":value}}})

def get_user(lex_user_id):
  return client.scan(TableName="users", FilterExpression="lex_user_id = :a", ExpressionAttributeValues={
        ':a': {
            'S': lex_user_id,
        }})["Items"]