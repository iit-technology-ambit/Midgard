"""
Slackbot controlls
Slack URL is in $SLACK_URL
"""
import requests
import os
import time
import dotenv

dotenv.load_dotenv('conf.env')

URL = os.getenv('SLACK_URL')

def new_spawn_msg(repo):
    '''
    Sends message of new repo spawning.
    '''
    requests.post(URL, json={'text': f'Deploying { repo }'})

def build_log_msg(repo):
    '''
    Send the build logs of the files
    '''
    try:
        return '```\n' + open(os.path.join(os.getenv("LOG_PATH"), repo + '.log'), 'r').read() + '```', 200
    except:
        return "Repo not found", 200