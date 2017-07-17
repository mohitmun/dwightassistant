import boto3


class ApiGateway:
  """docstring for LexRunTimeApi"""
  def __init__(self):
    self.client = boto3.client('apigateway')

  def create_rest_api():
    self.client.create_rest_api(name="dwight")

  def create_resource(res):
    return self.client.create_resource(restApiId='tn78yzlfic', parentId='8qf6wmxlph',pathPart=res)

  def put_method(method):
    return self.client.put_method(restApiId='tn78yzlfic', resourceId='r1iee2',httpMethod=method, authorizationType='NONE')

  def put_integration():
    return self.client.put_integration(restApiId='tn78yzlfic', resourceId='r1iee2',httpMethod='GET', authorizationType='NONE')

  def get_integration():
    return self.client.get_integration(restApiId='jefp0rl7th', resourceId='yab5da', httpMethod='GET')