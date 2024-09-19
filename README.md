# SDP Demo

Simple app to demonstrate Safe Deployment Practices. 

Prepared for [Prague DevOps Meetup](https://www.meetup.com/prague-devops-meetup/events/301615719/).

## Description

- `app.py` is web server, that load env vars
- envs vars (e.g. `FEATURE_A=10`) define features and time after which they will fail
- docker compose deploys 9 containers grouped in 3 rings
- nginx acts like a failover proxy for each ring
- `availability.py` monitors health status of rings
- `sdp.py` simulates build and release 

## How to run

Install `docker` with `docker compose` (new one).

Outside of the container:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Build `nginx` manually:

```
docker compose build 
```

## Helper commands

Build & run contianer with a `FEATURE_B` manually.

```
docker build --build-arg FEATURE_B=10 . -t sdp-app
docker run -p 7900:7900 -it sdp-app
```

Redeploy one container

```
docker compose stop ring_a_3
docker compose up -d ring_a_3
```

## Demo instructions

1. Run `sdp.py` once (no features) to have a build.
2. Run `availability.py` to see 100%.
3. Run `sdp.py` again to demo high availability (still no features).
4. Demo feature with large bake time to show failed deployment.
5. Demo small bake time, to get the low availability.
6. Recovery without features.
7. Demo same feature, but large bake time. No impact to last rings.
8. Demo feature being disabled in the initial ring.
