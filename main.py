import lex_models
import lambda_api
import api_gateway

region = "us-east-1"
account_no = "420758276632"
lambda_function_name = "dwight"
api_lex = lex_models.LexApi()
api_lambda = lambda_api.LambdaApi()
api_runtime = lex_models.LexRunTimeApi()
api_gateway = api_gateway.ApiGateway()

# api_lex.create_intent()
# api_lex.create_bot()
# api_gateway.set_up_dwight_gateway(region, account_no, lambda_function_name)