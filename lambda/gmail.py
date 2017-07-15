# event_method_mapping = {"Get"}
import utils

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  if underscore_name == "get_last_email_gmail":
    return get_last_email()

def get_last_email():
  return "this is last mail"