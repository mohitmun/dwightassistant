import lex_models
import lambda_api
import api_gateway
import boto3
region = "us-east-1"
account_no = "420758276632"
lambda_function_name = "dwight"
api_lex = lex_models.LexApi()
api_lambda = lambda_api.LambdaApi()
api_runtime = lex_models.LexRunTimeApi()
api_gateway = api_gateway.ApiGateway()

# iam_client = boto3.client('iam')
# iam_client.create_role(RoleName='LAMBDA_ROLE',AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Action": "sts:AssumeRole", "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}}]}')
# iam = boto3.resource('iam')
# role = iam.Role('LAMBDA_ROLE')
# response = role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess')
# api_lambda.create_function(lambda_function_name, role.arn)

def setup_bot():
  api_lex.create_slot_types()
  api_lex.create_intents()
  api_lex.create_bot()
  
# create channels
# api_gateway.set_up_dwight_gateway(region, account_no, lambda_function_name)
#todo what about dynamo permission we are in limbo
# api_lambda.add_permission(lambda_function_name, "lambda:*", "apigateway.amazonaws.com")
# add envs
# gmail scene