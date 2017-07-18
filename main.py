import lex_models
import lambda_api
import api_gateway
import boto3
import data
region = "us-east-1"
account_no = "420758276632"
bot_name = data.get_bot()["name"]
lambda_function_name = bot_name+"Lambda"
api_lex = lex_models.LexApi()
api_lambda = lambda_api.LambdaApi()
api_runtime = lex_models.LexRunTimeApi()
api_gateway = api_gateway.ApiGateway()


def setup_lambda():
  iam_client = boto3.client('iam')
  RoleName = bot_name+"_LAMBDA_ROLE"
  iam_client.create_role(RoleName=RoleName,AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Action": "sts:AssumeRole", "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}}]}')
  iam = boto3.resource('iam')
  role = iam.Role(RoleName)
  response = role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
  api_lambda.create_function(lambda_function_name, role.arn)
  api_lambda.add_permission(lambda_function_name, "lambda:*", "apigateway.amazonaws.com")
  api_lambda.add_permission(lambda_function_name, "lambda:*", "lex.amazonaws.com")

def setup_bot():
  api_lex.create_slot_types()
  api_lex.create_intents()
  api_lex.create_bot()

def setupdb():
  dclient = boto3.client('dynamodb')
  dclient.create_table(AttributeDefinitions=[{'AttributeName':'user_id', 'AttributeType':'S'}], TableName=bot_name, KeySchema=[{'AttributeName':'user_id', 'KeyType':'HASH'}], ProvisionedThroughput={'ReadCapacityUnits':1, 'WriteCapacityUnits':1})

def setup_gateway():
  return api_gateway.set_up_dwight_gateway(bot_name+"_api", region, account_no, lambda_function_name)
# setup_bot()
# setupdb()
# setup_lambda()

# create channels
#todo what about dynamo permission we are in limbo
# basic lamda policy scene
# gmail scene
# create gmail, spotify, uber apps or here take mine
# add envs
# set db name and auth url in env.py