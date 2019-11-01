from multiprocessing import Process, Queue
import pickle
import json
from collections import deque
import signal
from hookListen import run_on_proc
from builder import buildRepo
import os
import datetime

def signal_handler(sign, frame):
    print("Caught Kill Signal..........")
    raise KeyboardInterrupt

procs = Queue()
running_threads = {}


if __name__ == "__main__":    
    log_path = os.environ.get("LOG_PATH")
    op = open(os.path.join(log_path, "listener.log"), "a")
    op.write(f"[{datetime.datetime.now()}]\n")
    listener = Process(target=run_on_proc, args=(procs, op))
    listener.start()

    with open("whitelist.json", "r") as f:
        names = json.load(f)
        for name in names.keys():
            if name != "midgard":
                running_threads[name] = buildRepo(name)
            else:
                running_threads[name] = "midgard_main" #Dummy
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGABRT, signal_handler)
        while True:
            if not procs.empty():
                new_proc = procs.get(block=True)
                if new_proc in running_threads.keys():
                    running_threads[new_proc].terminate()
                    running_threads[new_proc] = buildRepo(new_proc)
                    
    except KeyboardInterrupt:
        #Exit gracefully
        listener.terminate()
        listener.join()

        for k in running_threads.keys():
            running_threads[k].terminate()

        exit(0)
