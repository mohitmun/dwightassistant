import os
lol = {
  "SPOTIFY_CLIENT_ID": "XXX", 
  "SPOTIFY_CLIENT_SECRET": "XXX",
  "GMAIL_CLIENT_ID": "XXX",
  "GMAIL_CLIENT_SECRET": "XXX",
  "UBER_CLIENT_ID": "XXX",
  "UBER_CLIENT_SECRET": "XXX",
  "SLACK_TOKEN": "XXX",
  "FB_TOKEN": "XXX",
  "FB_SECRET": "XXX",
  "BOT_NAME": "XXX",
  "OAUTH_APIGATEWAY_URL": "XXX",
  "LAMBDA_URI": "XXX"
}
for key in lol:
  os.environ[key] = lol[key]

def get_env():
  return lol

