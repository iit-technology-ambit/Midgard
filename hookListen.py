"""
Github webhook listener
"""
import hashlib
import hmac
import os
import pickle
from flask import Flask, request, abort, session, redirect, url_for, render_template
from dotenv import load_dotenv
from collections import deque
import json
import subprocess
from contextlib import redirect_stdout
from cheroot.wsgi import Server as WSGIServer
import slackbot

load_dotenv("conf.env")
procs = None
app = Flask(__name__)
app.config["GITHUB_SECRET_TOKEN"] = os.environ.get("GITHUB_SECRET_TOKEN")
app.config["ADMIN_PIN"] = os.environ.get("MIDGARD_ADMIN_PIN")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route("/github/<repo>", methods=["GET", "POST"])
def getRequest(repo):
    global procs
    valid = True
    raw_data = request.get_data()
    try:
        sha_name, signature = request.headers['X-Hub-Signature'].split("=")
        if sha_name != "sha1":
            valid = False
        else:
            mac = hmac.new(app.config["GITHUB_SECRET_TOKEN"].encode(), msg=raw_data, digestmod=hashlib.sha1)
            if not hmac.compare_digest(mac.hexdigest(), signature):
                valid = False
    except:
        valid = False
    if valid:
        if procs is not None:
            procs.put(repo)
    
        return "Payload processed", 200
    else:
        abort(403)

@app.route("/build/<repo>")
def directBuildEndpoint(repo):
    if 'ADMIN_PIN' in session and session['ADMIN_PIN'] == app.config['ADMIN_PIN']:
        global procs
        if procs is not None:
            procs.put(repo)
        return redirect("/dashboard")
    else:
        abort(403)

@app.route("/dashboard")
def dashHandle():
    if 'ADMIN_PIN' in session and session['ADMIN_PIN'] == app.config['ADMIN_PIN']:
        f = open("whitelist.json", "r")
        names = json.load(f)
        f.close()
        return render_template("dashboard.html", names=names)
    else:
        return redirect("/")

@app.route("/")
def landing():
    if 'ADMIN_PIN' in session and session['ADMIN_PIN'] == app.config['ADMIN_PIN']:
        return redirect("/dashboard")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_user():
    session['ADMIN_PIN'] = request.form['pin']
    return redirect("/dashboard")

@app.route("/logout")
def logout_user():
    session['ADMIN_PIN'] = ""
    return redirect("/")

app.route("/slack/logs", methods=["POST"])
def show_logs():
    return slackbot.build_log_msg(request.form['text'])

    
def run_on_proc(proc_q, fp):
    global procs
    global app
    procs = proc_q
    server = WSGIServer(('127.0.0.2', 5918), app, numthreads=4)
    server.start()

if __name__ == "__main__":
    app.run(debug=True)
