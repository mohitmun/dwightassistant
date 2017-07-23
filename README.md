# DwightAssistant
Project I built for AWS Chatbot challenge
#### [Here](https://www.youtube.com/playlist?list=PLQcGlLJQrlIAZ6Rh2gptL7n-dF749-2C4) is full demo playlist

![Spotify](spot.gif)
![Gmail](gmail.gif)
![Uber](uber.gif)

## What it does

Dwight is a chatbot assistant that helps you connect to multiple services by adding them via OAuth. The services that I have added for now are:

Gmail : Access your mailbox through commands like "Show my unread emails", "Whats last starred mail", "Show mails after 17 july", "Show all emails sent by projjol", Send, forward, reply and other actions on mail

Spotify : Developing this skill was really fun and now I can control my music on Spotify via this new skill. I can search for new music. I can also play specific songs and artists using this skill

Uber: Travelling takes an important part of our day and organising this is efficiently is a major concern for me. Using this skill I can now book an Uber and constantly view the current prices.

###Key Features
1. One command and deploy whole stack to AWS. It leverages boto3 client to create/edit/update/delete resources in AWS
2. Highly extendable architecture. Its extremely easy to add new services which uses Oauth to give access to user data
3. Search mails by keywords, time, name of user who sent it, unread, starred etc
4. Play music by artist name, track name and album. All player actions like play, pause etc
5. Keep context between channels. Support you are chatting with Dwight on Facebook and you switch to Dwight slack, It will remember your last conversation and continue it

## Self-Hosting
  - clone the repo
  - Make sure aws credentials are in ~/.aws/credentials
  - Run setup_stack() in main.py, and note api gateway URL, you will require it in env.py 
  - setup bot channels in aws lex
  - set required fields in env.py
  - set redirect uri in client apps
  - Uber apis are sandboxed so change it to api.uber.com
  - After setting gmail client you will have to do this https://stackoverflow.com/questions/44329890/error-invalid-scope-this-app-hasnt-been-verified-to-access

## Note
- If you want to start using quickly with out creating any service apps, ping me at mohmun16@gmail.com, I will share client_id and client_secret with you. Remember access_token will still be on your server so I wont have any acess to it so you own your data
- There are lots of bugs (built within three day).also I'm new to aws so to get job done quickly, permissions setup are not proper in main.py


## TODO

- Integrate Google drive, Youtube, Reddit, Facebook, Twitter, Google Maps etc.
- For Gmail integration, push notification for incoming mails 
- Developer mode - Train lex through boto3 client.
