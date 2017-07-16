import boto3
import string
import random
client = boto3.client('dynamodb')

def add_user(lex_user_id):
  random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
  client.put_item(TableName="users", Item={"user_id": {"S": random_id}, "lex_user_id": {"S": lex_user_id}})
  return random_id