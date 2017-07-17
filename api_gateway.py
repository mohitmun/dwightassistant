import boto3


class ApiGateway:
  """docstring for LexRunTimeApi"""
  def __init__(self):
    self.client = boto3.client('apigateway')

  def create_rest_api(self, name):
    return self.client.create_rest_api(name=name)

  def get_resources(self, restApiId):
    return self.client.get_resources(restApiId=restApiId)

  def create_resource(self, restApiId, parentId, res):
    return self.client.create_resource(restApiId=restApiId, parentId=parentId, pathPart=res)

  def put_method(self, restApiId, resourceId, method):
    return self.client.put_method(restApiId=restApiId, resourceId=resourceId,httpMethod=method, authorizationType='NONE')

  def put_integration(self, restApiId, resourceId, httpMethod, uri):
    return self.client.put_integration(restApiId=restApiId, resourceId=resourceId,httpMethod=httpMethod, type="AWS_PROXY",uri=uri, integrationHttpMethod='GET')

  def get_integration(self, restApiId, resourceId):
    return self.client.get_integration(restApiId=restApiId, resourceId=resourceId, httpMethod='GET')

  def create_deployment(self, restApiId, stageName):
    return self.client.create_deployment(restApiId=restApiId,stageName=stageName)

  def set_up_dwight_gateway(self, aws_region, aws_acct_id, lambda_function):
    new_api = self.create_rest_api("Dwight2")
    restApiId = new_api["id"]
    resources = self.get_resources(restApiId)
    root_id = resources["items"][0]["id"]
    dwight_resources = ["spotify" ,"connect-spotify" ,"gmail" ,"connect-gmail" ,"uber" ,"connect-uber"]
    for resource_name in dwight_resources:
      new_resource = self.create_resource(restApiId, root_id, resource_name)
      self.put_method(restApiId, new_resource["id"], "GET")
      uri = "arn:aws:apigateway:{0}:lambda:path/2015-03-31/functions/arn:aws:lambda:{0}:{1}:function:{2}/invocations".format(aws_region, aws_acct_id, lambda_function)
      self.put_integration(restApiId, new_resource["id"], "GET", uri)
    return self.create_deployment(restApiId, "prod")