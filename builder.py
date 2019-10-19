"""
Automated building function
------------------------------

All output logs will be redirected to the environment variable: LOG_PATH
"""
import json
import os
import signal
import subprocess
from dotenv import load_dotenv

def buildRepo(name):
    fp = open("whitelist.json", "r")
    whitelist = json.load(fp)
    fp.close()
    load_dotenv("conf.env")
    log_path = os.environ.get("LOG_PATH")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
        open(os.path.join(log_path, "pid.json"), "w")
    pids = dict()
    with open(os.path.join(log_path, "pid.json"), "r") as f:
        dump = f.read()
        try:
            pids = json.loads(dump)
        except:
            pass
        
    if name in whitelist.keys():
        curr_path = os.getcwd()
        #Kill the existing process
        if name in pids.keys():
            try:
                os.kill(pids[name], signal.SIGTERM)
            except:
                pass
         
        #Spawn new process
        log = open(os.path.join(log_path, (name + ".log")), "a")
        os.chdir(whitelist[name]['path'])
        os.system("git pull")
        proc = subprocess.Popen(whitelist[name]['cmd'].split(";"), shell=True, stdout=log)
        
        os.chdir(curr_path)
        pids[name] = proc.pid
        with open(os.path.join(log_path, "pid.json"), "w") as f:
            json.dump(pids, f)


