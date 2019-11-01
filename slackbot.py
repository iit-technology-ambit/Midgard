"""
Slackbot controlls
Slack URL is in $SLACK_URL
"""
import requests
import os

URL = os.getenv('SLACK_URL')

def new_spawn_msg(repo):
    '''
    Sends message of new repo spawning.
    '''
    requests.post(URL, json={'text': f'Deploying { repo }'})    