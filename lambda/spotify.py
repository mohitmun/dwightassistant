from requests_oauth2 import OAuth2
import os
import utils
import dynamodb
import json
from urllib import quote, urlencode
import base64
import base_service
service = "spotify"
base_service = base_service.BaseService(service)
redirect_uri = utils.get_api_auth_url(service)
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
oauth2_handler = OAuth2(client_id, client_secret, "https://accounts.spotify.com/", redirect_uri, "authorize", "api/token")
#todo cut down some permission
authorization_url = oauth2_handler.authorize_url('user-read-playback-state playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-follow-read user-follow-modify user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state') + "&response_type=code"

def save_access_token(event):
  code = event["queryStringParameters"]["code"]
  user_id = event["headers"]["Cookie"].split("=")[-1]
  res = get_and_save_access_code(code, user_id)
  return {
    'statusCode': '200',
    'body': json.dumps({"message": "Spotify Connected!",  "event": event, "res": res}),
    'headers': {
        'Content-Type': 'application/json',
    },
  }

def get_and_save_access_code(code, user_id):
  base64_id_secret = base64.b64encode("{0}:{1}".format(os.environ["SPOTIFY_CLIENT_ID"], os.environ["SPOTIFY_CLIENT_SECRET"]))
  command = "curl -d 'grant_type=authorization_code' -d 'code={0}' -d 'redirect_uri={1}' -H \"Authorization: Basic {2}\" \"https://accounts.spotify.com/api/token\"".format(code, quote(redirect_uri), base64_id_secret, 'utf-8')
  print(command)
  return base_service.get_and_save_access_code(user_id, command)

def redirect_to_auth(event):
  return base_service.redirect_to_auth(event, authorization_url)

def refresh_access_token(user):
  print("refresing token")
  command = "curl https://accounts.spotify.com/api/token -d 'refresh_token={0}' -d 'client_id={1}' -d 'client_secret={2}' -d 'grant_type=refresh_token'".format(base_service.get_refresh_token(user), client_id, client_secret)
  user = base_service.get_and_save_access_code(base_service.get_user_id(user), command)
  return user

def handle(event):
  currentIntent = event["currentIntent"]["name"]
  underscore_name = utils.convert_camelcase(currentIntent)
  user = base_service.handle(event)
  access_token = base_service.get_access_token(user)
  if access_token != None:
    if base_service.token_expired(user):
      user = refresh_access_token(user)
    if underscore_name == "play_spotify":
      return play_spotify_intent(user, event)
    if underscore_name == "stop_spotify":
      return stop_spotify_intent(user, event)
  else:
    return base_service.send_api_auth_link(user["user_id"]["S"])

def token_expired(user):
  return base_service.token_expired(user)

# event = {"currentIntent": {"slots": {"album": "", "song": "", "artist": ""}}}
def play_spotify_intent(user, event):
  slots = event["currentIntent"]["slots"]
  song = slots["song"]
  album = slots["album"]
  artist = slots["artist"]
  if song != None:
    if artist != None:
      searched_song = search_song_by_artist(user, song, artist)
    else:  
      searched_song = search_song(user, song)
    if searched_song:
      return play_tracks_intent(user, [searched_song["uri"]])
    else:
      #todo remove no result json
      return utils.send_message("No results found! slots:" + json.dumps(slots))
  elif album != None:
    searched_album = search_album(user, album)
    if searched_album:
      return play_context_intent(user, searched_album["uri"])
    else:
      return utils.send_message("No results found! slots:" + json.dumps(slots))
  elif artist != None:
    searched_artist = search_artist(user,artist)
    if searched_artist:
      return play_context_intent(user, searched_artist["uri"])
    else:
      return utils.send_message("No results found! slots:" + json.dumps(slots))
  command = "-X PUT 'https://api.spotify.com/v1/me/player/play'"
  res = base_service.authorized_curl(command, user)
  return utils.send_message(json.dumps(res) + " event: " + json.dumps(event))

def stop_spotify_intent(user, event):
  command = "-X PUT 'https://api.spotify.com/v1/me/player/play'"
  res = base_service.authorized_curl(command, user)
  return utils.send_message(json.dumps(res) + " event: " + json.dumps(event))

def test_user():
  return dynamodb.get_item("XB29T8")

def search_song_by_artist(user, track_q, artist_q):
  items = search_item(user, "track:{}%20artist:{}".format(track_q, artist_q), "track")["tracks"]["items"]
  if len(items) > 0:
    return items[0]
  else:
    return None

def play_tracks_intent(user, uris):
  data = {"uris": uris}
  command = "-X PUT 'https://api.spotify.com/v1/me/player/play' -H 'Content-Type: application/json' --data '{}'".format(json.dumps(data))
  res = base_service.authorized_curl(command, user)
  return utils.send_message("played track: " + json.dumps(uris) + " res: " + json.dumps(res))

def play_context_intent(user, context_uri):
  data = {"context_uri": context_uri}
  command = "-X PUT 'https://api.spotify.com/v1/me/player/play' -H 'Content-Type: application/json' --data '{}'".format(json.dumps(data))
  res = base_service.authorized_curl(command, user)
  return utils.send_message("playing context: " + json.dumps(context_uri) + " res: " + json.dumps(res))

def search_album(user, q):
  res = search_item(user, q, "album")
  items = res["albums"]["items"]
  if len(items) > 0:
    return items[0]
  else:
    return None

def search_artist(user, q):
  res = search_item(user, q, "artist")
  items = res["artists"]["items"]
  if len(items) > 0:
    return items[0]
  else:
    return None

def search_song(user, q):
  res = search_item(user, q, "track")
  items = res["tracks"]["items"]
  if len(items) > 0:
    return items[0]
  else:
    return None

def get_album_songs(album_id, user):
  command = "-X GET https://api.spotify.com/v1/albums/{}/tracks".format(album_id)
  res = base_service.authorized_curl(command, user)
  return res

def search_item(user, q, q_type):
  # Valid types are: album, artist, playlist, and track.
  q = q.replace(" ", "%20")
  q_type = q_type.replace(" ", "+")
  url = "https://api.spotify.com/v1/search?q={}&type={}&limit=10".format(q, q_type)
  command = "-X GET '{}'".format(url)
  res = base_service.authorized_curl(command, user)
  return res
# curl -X PUT "https://api.spotify.com/v1/me/player/play" -H "Authorization: Bearer BQCF5bnU0EY0uTpkoC3HUl-66YJjZXu5ULt503BHEP-9WkMcro2xJcO4atyxl04hIdW4z_aLdHwslDX40oJSAsmX2h6e99Dvv4EOAl7Xj4dM_utbPJf9Adk0fuD0yas_vfPTjpjgfdmQYkE"

# https://accounts.spotify.com/authorize/?client_id=a7ed7ac582c4421397e4336a9339d849&response_type=code&redirect_uri=https%3A%2F%2Fmamam.com&scope=user-modify-playback-state




# \curl -d grant_type=authorization_code -d code=AQBpjD88SGOBw7k5G1C64tC-6qEZnwSSQl56t-9EPKZ58ZvaD4xdY9GO_xQbHBM5M0bEuKFqCkNlFtlTOf_NQFVi1K_YhAWuL_xKTRcmN3Oym62qFv-f-JTL2IRFkH6b0eFMuigb9X-toElrDV3gBLTAlX8UNkoo4voGNPxJAAOlp_nulVJh-gJkNWG4Qvjvp3tGxg6pA7_kd5UrLxB6G5_W2w -d redirect_uri=https%3A%2F%2Fmamam.com -H "Authorization: Basic YTdlZDdhYzU4MmM0NDIxMzk3ZTQzMzZhOTMzOWQ4NDk6NmRkNTQ4MGY2NzNkNGZlZThmN2QyMjU3MzdhOWViN2E=" "https://accounts.spotify.com/api/token"


# {"access_token":"BQCF5bnU0EY0uTpkoC3HUl-66YJjZXu5ULt503BHEP-9WkMcro2xJcO4atyxl04hIdW4z_aLdHwslDX40oJSAsmX2h6e99Dvv4EOAl7Xj4dM_utbPJf9Adk0fuD0yas_vfPTjpjgfdmQYkE","token_type":"Bearer","expires_in":3600,"refresh_token":"AQAWdn2eyEmmM8e1-QpSkrQjcrCoA7YS2srYsV_G5enD6CSazPm8kDRi8hYrbmrqQjG8cO_QvcxM0THV2leLEpcOKGFzdc37zjSLzbJ0MFS0IjGZZakk99yvrdfScTwE1hA","scope":"user-modify-playback-state"}