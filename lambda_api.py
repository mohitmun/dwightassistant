import os
import zipfile
import boto3
import env
class LambdaApi:
  def __init__(self):
    self.client = boto3.client('lambda')

  def list_functions(self):
    return self.client.list_functions()
  
  def update_function_code(self):
    # zip_file = zipfile.ZipFile("lambda.zip", "w")  
    # zip_file.write("lambdama/gmail.py",compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile('lambda.zip', 'w') as myzip:
    #   for f in os.listdir("lambda"):   
    #     myzip.write("lambda/" + f, f)
      for root, dirs, files in os.walk('lambda'):
        for f in files:
          if ".git" not in os.path.join(root, f):
            myzip.write(os.path.join(root, f), os.path.join(root, f)[7:])
    # return 1
    return self.client.update_function_code(FunctionName="test", ZipFile=open("lambda.zip", "rb").read())
  
  def add_permission(self):
    return self.client.add_permission(FunctionName="test",StatementId="ID-12chutest", Action= "lambda:*", Principal="lex.amazonaws.com")

  def update_function_configuration(self):
    return self.client.update_function_configuration(FunctionName= "test", Environment={'Variables': env.get_env()})
    #     FunctionName='string',
    # StatementId='string',
    # Action='string',
    # Principal='string',
    # SourceAccount='string',
    # EventSourceToken='string',
    # Qualifier='string'
