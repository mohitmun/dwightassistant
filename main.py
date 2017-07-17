import lex_models
import lambda_api
import api_gateway
print("chus1")
api_lex = lex_models.LexApi()
api_lambda = lambda_api.LambdaApi()
api_runtime = lex_models.LexRunTimeApi()
api_gateway = api_gateway.ApiGateway()

# api_lex.create_intent()
# api_lex.create_bot()