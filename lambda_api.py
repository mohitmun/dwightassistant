import os
import zipfile
import boto3
import env
import time
class LambdaApi:
  def __init__(self):
    self.client = boto3.client('lambda')

  def list_functions(self):
    return self.client.list_functions()
  
  def update_function_code(self, FunctionName):
    # zip_file = zipfile.ZipFile("lambda.zip", "w")  
    # zip_file.write("lambdama/gmail.py",compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile('lambda.zip', 'w') as myzip:
    #   for f in os.listdir("lambda"):   
    #     myzip.write("lambda/" + f, f)
      for root, dirs, files in os.walk('lambda'):
        for f in files:
          myzip.write(os.path.join(root, f), os.path.join(root, f)[7:])
    # return 1
    print("Uploading started")
    res = self.client.update_function_code(FunctionName=FunctionName, ZipFile=open("lambda.zip", "rb").read())
    try:
      os.system('osascript -e \'display notification "Uplading done" with title "ApiGateway"\'')
    except Exception as e:
      print("error")
    return res
  
  def add_permission(self, FunctionName, Action, Principal):
    return self.client.add_permission(FunctionName=FunctionName,StatementId="ID-{0}-{1}".format(FunctionName, int(time.time())), Action= Action, Principal=Principal)

  def update_function_configuration(self, FunctionName):
    return self.client.update_function_configuration(FunctionName= FunctionName, Environment={'Variables': env.get_env()})
    #     FunctionName='string',
    # StatementId='string',
    # Action='string',
    # Principal='string',
    # SourceAccount='string',
    # EventSourceToken='string',
    # Qualifier='string'
