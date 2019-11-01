[Logo](static/square-logo.png)

# Midgard

This is the Continous Deployment System of IIT Technology Ambit.

# Specifications

Whenever there is a new commit in the master branch of the repos of the Ambit, that change will be pulled by the Ambit Server.
It will be built there locally and will be deployed to production according to the build script provided for that repo.

Currently, it is watching:

- `Syphus`
- `Apsara 2.0`

It provides a dashboard for remote admin access and redeployment. It integrates with a private Slack app: `Midgard Notifier` and sends messages on rebuild. It can also send build logs of a repo to slack if an user runs the slash command `/logs repo`

# Under the hood

It runs a mini Flask server waiting for Github webhook request (with some `SECRET KEY`). Then midgard will run `git pull` on the repo saved in the server and run the build script. We use the Cheroot WSGI server to deploy the app in production.

# Usage

Fill out the necessary environment variables given in `conf.env.template` and save as `conf.env`. Similarly, fill up all your required processes in the format given in `whitelist.json.template` and save as `whitelist.json`. 

### Example entry of `whitelist.json`

```json
"blogger": {
        "path": "/home/grapheo12/fb",
        "cmd": "pwd && source venv/bin/activate && python run.py",
        "branch": "master"
    }
```

Remember to always use absolute paths.

Create a new virtual environment by `virtualenv` and install all the dependencies in `requirement.txt`.

Run the server by: `python3 main.py`

In the Github repos, go to `Settings > Webhooks`. Add `https://midgard.iit-techambit.in/github/[repo name as in whitelist.json]` as Webhook. In the Secret Key section, use `GITHUB_SECRET_TOKEN` specified in `conf.env`.

You can redeploy your projects at will by opening the Midgard dashboard, `https://midgard.iit-techambit.in/dashboard` by logging in using the admin pin saved in `conf.env`.

