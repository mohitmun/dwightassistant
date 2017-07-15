import zipfile
import boto3
class LambdaApi:
  def __init__(self):
    self.client = boto3.client('lambda')

  def list_functions(self):
    return self.client.list_functions()
  
  def update_function_code(self):
    zipfile.ZipFile("lambda.zip", "w").write("lambda_function.py",compress_type=zipfile.ZIP_DEFLATED)
    return self.client.update_function_code(FunctionName="test", ZipFile=open("lambda.zip", "rb").read())
  
  def add_permission(self):
    return self.client.add_permission(FunctionName="test",StatementId="ID-12chutest", Action= "lambda:*", Principal="lex.amazonaws.com")

    #     FunctionName='string',
    # StatementId='string',
    # Action='string',
    # Principal='string',
    # SourceAccount='string',
    # EventSourceToken='string',
    # Qualifier='string'
