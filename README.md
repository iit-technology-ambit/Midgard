# Midgard

This is the Continous Deployment System of IIT Technology Ambit.

# Specifications

Whenever there is a new commit in the master branch of the repos of the Ambit, that change will be pulled by the Ambit Server.
It will be built there locally and will be deployed to production according to the build script provided for that repo.

Currently, it is watching:

- `Syphus`
- `Apsara 2.0`

In future, it may also provide a dashboard for remote management.

# Under the hood

It runs a mini Flask server waiting for Github webhook request (with some `SECRET KEY`). Then midgard will run `git pull` on the repo saved in the server and run the build script.