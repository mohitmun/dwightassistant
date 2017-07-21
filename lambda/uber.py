# event_method_mapping = {"Get"}
from requests_oauth2 import OAuth2
import os
import utils
import dynamodb
import json
from urllib import quote, urlencode
import base64
import base_service
service = "uber"
base_service = base_service.BaseService(service)
redirect_uri = utils.get_api_auth_url(service)
client_id = os.environ['UBER_CLIENT_ID']
client_secret = os.environ['UBER_CLIENT_SECRET']
auth_base = "https://login.uber.com/oauth/v2/"
oauth2_handler = OAuth2(client_id, client_secret, auth_base, redirect_uri, "authorize", "token")
authorization_url = oauth2_handler.authorize_url('request places profile history all_trips') + "&response_type=code"

def get_and_save_access_code(code, user_id):
  command = "curl https://login.uber.com/oauth/v2/token -F 'code={0}' -F 'client_id={1}' -F 'client_secret={2}' -F 'redirect_uri={3}' -F 'grant_type=authorization_code'".format(code, client_id, client_secret, redirect_uri)
  print(command)
  return base_service.get_and_save_access_code(user_id, command)

def save_access_token(event):
  code = event["queryStringParameters"]["code"]
  user_id = event["headers"]["Cookie"].split("=")[-1]
  res = get_and_save_access_code(code, user_id)
  return {
    'statusCode': '200',
    'body': json.dumps({"message": "Uber Connected, Now you can go back to chatbot!"}),
    'headers': {
        'Content-Type': 'application/json',
    },
  }

def redirect_to_auth(event):
  return base_service.redirect_to_auth(event, authorization_url)

def get_authorization_url():
  return authorization_url

def refresh_access_token(user):
  command = "curl https://login.uber.com/oauth/v2/token -F 'refresh_token={0}' -F 'client_id={1}' -F 'client_secret={2}' -F 'grant_type=refresh_token'".format(base_service.get_refresh_token(user), client_id, client_secret)
  print("refresing token")
  res = os.popen(command).read()
  print(command)
  print(res)
  base_service.save_credentials(base_service.get_user_id(user), res)
  return res

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  user = base_service.handle(event)
  access_token = base_service.get_access_token(user)
  if access_token != None:
    if base_service.token_expired(user):
      refresh_access_token(user)
    if underscore_name == "book_cab_uber":
      return book_cab_uber(user, event)
  else:
    return base_service.send_api_auth_link(base_service.get_user_id(user))

def token_expired(user):
  return base_service.token_expired(user)

sandbox_url = "https://sandbox-api.uber.com/"

products = {
    
      "83941b0d-4be1-4979-a9c0-f0af5ee2b89b":{
      "display_name": "uberGO",
      "description": "Smaller. Smarter. Cheaper."}
    ,
    
      "a2b80c84-8d64-4c20-b731-6bf07d32cc9a":{
      "display_name": "uberX",
      "description": "THE LOW-COST UBER"}
    ,
    
      "d5c3d5fe-883f-4105-99e4-fcb9ae46a988":{
      "display_name": "UberXL",
      "description": "ROOM FOR EVERYONE"}
    ,
    
      "65849e62-1044-4b64-ac22-7451023f7eaf":{
      "display_name": "UberBLACK",
      "description": "THE ORIGINAL UBER"}
  }

def send_fares(user, event, fares_and_args):
  res = ""
  fares = fares_and_args["fares"]
  fare_slot = event["currentIntent"]["slots"]["fare_slot"]
  fare_session = {}
  for fare in fares:
    car_name = fare["product"]["display_name"]
    fare_id = fare["fare"]["fare_id"]
    if fare_slot != None and car_name.lower() == fare_slot.lower():
      return book_uber(user, fare_id, **fares_and_args["args"])
    fare_session[car_name.lower()] = fare_id
    fare_value = fare["fare"]["display"]
    pickup_estimate = "{} mins".format(fare["pickup_estimate"])
    duration = "{} mins".format(fare["trip"]["duration_estimate"]/60) 
    res = res + "{}\nFare: {}\nPickup in: {}\nDuration: {}\n\n".format(car_name, fare_value.encode('utf-8').strip(), pickup_estimate, duration)
  res = "Which cab should I book for you?\n\n{}".format(res)
  return elicit_slot(event["currentIntent"]["slots"], "fare_slot", message=res, session={"fare_session": json.dumps(fare_session), "args": json.dumps(fares_and_args["args"])})

def elicit_slot(slots, slot, **args):
  res = {"dialogAction": {
    "type": "ElicitSlot",
    "intentName": "BookCabUber",
    "slots": slots,
    "slotToElicit" : slot
  }}
  if "message" in args:
    res["dialogAction"]["message"] = {
        "contentType": "PlainText",
        "content": args["message"]
      }
  if "session" in args:
    res["sessionAttributes"] = args["session"]
  return res

def book_cab_uber(user, event):
  slots = event["currentIntent"]["slots"]
  fare_slot = event["currentIntent"]["slots"]["fare_slot"]
  if "sessionAttributes" in event and fare_slot != None:
    if fare_slot in event["sessionAttributes"]:
      return book_uber(user, json.loads(event["sessionAttributes"]["fare_session"])[fare_slot], json.loads(event["sessionAttributes"]["args"]))
  if slots["from_work_slot"] != None:
    if slots["to_home_slot"] != None:
      return send_fares(user, event, get_fares_from_work_to_home(user))
    else:
      if slots["to_postal_address_slot"] != None:
        latlong = utils.get_latlng(slots["to_postal_address_slot"])
        lat = latlong["lat"]
        lng = latlong["lng"]
        return send_fares(user, event, get_fares_from_work_to(user, lat, lng))
      else:
        return elicit_slot(event["currentIntent"]["slots"], "to_postal_address_slot")
  else:
    if slots["from_postal_address_slot"] != None:
      latlong = utils.get_latlng(slots["from_postal_address_slot"])
      start_lat = latlong['lat']
      start_lng = latlong['lng']
      if slots["to_postal_address_slot"] != None:
        latlong = utils.get_latlng(slots["to_postal_address_slot"])
        end_lat = latlong['lat']
        end_lng = latlong['lng']
        return send_fares(user, event, get_fares(user, start_latitude=start_lat, start_longitude=start_lng, end_latitude= end_lat, end_longitude= end_lng))
      else:
        if slots["to_work_slot"] != None:
          return send_fares(user, event, get_fares_to_work_from(user, start_lat, start_lng))
        else:
          if slots["to_home_slot"] != None:
            return send_fares(user, event, get_fares_to_home_from(user, start_lat, start_lng))
          else:
            return elicit_slot(event["currentIntent"]["slots"], "to_postal_address_slot")
    
    else:
      if slots["from_home_slot"] != None:
        if slots["to_work_slot"] != None:
          return send_fares(user, event, get_fares_from_home_to_work(user))
        else:
          if slots["to_postal_address_slot"] != None:
            temp = utils.get_latlng(slots["to_postal_address_slot"])
            end_lat = temp['lat']
            end_lng = temp['lng']    
            return send_fares(user, event, get_fares_from_home_to(user, end_lat,end_lng))
          else:
            return elicit_slot(event["currentIntent"]["slots"], "to_postal_address_slot")
      else:
        return elicit_slot(event["currentIntent"]["slots"], "from_postal_address_slot")

      # from_postal_address_slot
      # from_work_slot
      # from_home_slot
      # to_postal_address_slot
      # to_work_slot
      # to_home_slot
      # fare_slot
  return utils.send_message("uber booked")

def get_products(user, latitude, longitude):
  res =  base_service.authorized_curl("-X GET -H 'Content-Type: application/json' 'https://sandbox-api.uber.com/v1.2/products?latitude={}&longitude={}'".format(latitude, longitude), user)
  return res

def get_place(user,place_id):
  res =  base_service.authorized_curl("-X GET -H 'Content-Type: application/json' 'https://sandbox-api.uber.com/v1.2/places/{}'".format(place_id), user)
  latlong = utils.get_latlng(res["address"])
  res["lat"] = latlong["lat"]
  res["lng"] = latlong["lng"]
  return res

def get_fares_from_home_to(user, latitude, longitude):
  return get_fares(user, start_place_id="home", end_latitude=latitude, end_longitude=longitude)

def get_fares_from_work_to(user, latitude, longitude):
  return get_fares(user, start_place_id="work", end_latitude=latitude, end_longitude=longitude)

def get_fares_to_home_from(user, latitude, longitude):
  return get_fares(user, end_place_id="home", start_latitude=latitude, start_longitude=longitude)

def get_fares_to_work_from(user, latitude, longitude):
  return get_fares(user, end_place_id="work", start_latitude=latitude, start_longitude=longitude)

def get_fares_from_home_to_work(user):
  return get_fares(user, start_place_id="home", end_place_id="work")

def get_fares_from_work_to_home(user):
  return get_fares(user, start_place_id="work", end_place_id="home")

def get_fares(user, **args):
  s = {}
  if "start_place_id" in args:
    s["start_place_id"] = args["start_place_id"]
    if "end_place_id" in args:
      s["end_place_id"] = args["end_place_id"]
    else:
      s["end_latitude"] = args["end_latitude"]
      s["end_longitude"] = args["end_longitude"]
  else:
    if "end_place_id" in args:
      s = {"start_latitude": args['start_latitude'], "start_longitude": args["start_longitude"] ,"end_place_id": args["end_place_id"]}
    else:
      s = {"start_latitude": args['start_latitude'], "start_longitude": args["start_longitude"], "end_latitude": args["end_latitude"], "end_longitude": args["end_longitude"]}
  if "product" in args:
    s["product_id"] = args["product"]["product_id"]
    res = base_service.authorized_curl("-X POST -H 'Content-Type: application/json' 'https://sandbox-api.uber.com/v1.2/requests/estimate' -d '{}'".format(json.dumps(s)), user)
    res["product"] = args["product"]
    fares = [res]
  else:
    res_array = []
    if "start_place_id" in args:
      place_details = get_place(user,args["start_place_id"])
      products = get_products(user, place_details["lat"], place_details["lng"])
    else:
      products = get_products(user, args["start_latitude"], args["start_longitude"])
    for product in products["products"][:2]:
      s["product_id"] = product["product_id"]
      res = base_service.authorized_curl("-X POST -H 'Content-Type: application/json' 'https://sandbox-api.uber.com/v1.2/requests/estimate' -d '{}'".format(json.dumps(s)), user)
      res["product"] = product
      res_array.append(res)
    fares = res_array
  result = {"fares": fares, "args": args}
  return result

def book_uber(user, fare_id, **args):
  s = {}
  if "start_place_id" in args:
    s["start_place_id"] = args["start_place_id"]
    if "end_place_id" in args:
      s["end_place_id"] = args["end_place_id"]
    else:
      s["end_latitude"] = args["end_latitude"]
      s["end_longitude"] = args["end_longitude"]
  else:
    if "end_place_id" in args:
      s = {"start_latitude": args['start_latitude'], "start_longitude": args["start_longitude"] ,"end_place_id": args["end_place_id"]}
    else:
      s = {"start_latitude": args['start_latitude'], "start_longitude": args["start_longitude"], "end_latitude": args["end_latitude"], "end_longitude": args["end_longitude"]}
  s["fare_id"] = fare_id
  res = base_service.authorized_curl("-X POST -H 'Content-Type: application/json' 'https://sandbox-api.uber.com/v1.2/requests' -d '{}'".format(json.dumps(s)), user)
  if "status" in res:
    return utils.send_message("Uber booked!\nStatus:{}\nDriver:{}\nVehicle:{}".format(res['status'], res["driver"], res["vehicle"]))
  elif "errors" in res:
    return utils.send_message("Title:{}".format(res["errors"][0]["title"]))

def get_current(user):
  res = base_service.authorized_curl("-X GET -H 'Content-Type: application/json' 'https://sandbox-api.uber.com/v1.2/requests/current'", user)
  return res
