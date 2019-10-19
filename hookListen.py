"""
Github webhook listener
"""
import hashlib
import hmac
import os
from flask import Flask, request, abort
from dotenv import load_dotenv
from builder import buildRepo

load_dotenv("conf.env")

app = Flask(__name__)
app.config["GITHUB_SECRET_TOKEN"] = os.environ.get("GITHUB_SECRET_TOKEN")
@app.route("/<repo>", methods=["GET", "POST"])
def getRequest(repo):
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
        print("Received valid payload")
        buildRepo(repo)
        return "Payload processed", 200
    else:
        abort(403)

if __name__ == "__main__":
    app.run(debug=True)