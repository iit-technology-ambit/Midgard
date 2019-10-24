"""
Automated building function
------------------------------

All output logs will be redirected to: $LOG_PATH/repo.log
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

    proc_list = open(os.path.join(log_path, "pid.json"), "a+")
    proc_list.seek(0)
    dump = proc_list.read()
    try:
        pids = json.loads(dump)
    except:
        pass
        
    if name in whitelist.keys():
        #Kill the existing process
        if name in pids.keys():
            try:
                os.kill(pids[name], signal.SIGTERM)
            except:
                pass
         
        #Spawn new process
        log = open(os.path.join(log_path, (name + ".log")), "a")
        subprocess.call([f"cd { whitelist[name]['path'] } && git checkout { whitelist[name]['branch'] } && git pull origin { whitelist[name]['branch'] }"], shell=True)
        cmd = f"cd { whitelist[name]['path'] } && " + whitelist[name]['cmd']
        proc = subprocess.Popen([cmd], shell=True, stdout=log, stderr=log)
        pids[name] = proc.pid
        proc_list.truncate(0)
        json.dump(pids, proc_list)

        return proc


