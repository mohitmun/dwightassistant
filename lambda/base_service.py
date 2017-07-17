def redirect_to_auth(event, authorization_url):
  user_id = event["queryStringParameters"]["user_id"]
  return {
    'statusCode': '302',
    'headers': {
        'Location': authorization_url,
        'Set-Cookie': 'user_id='+ user_id
    },
  }
