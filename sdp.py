import os
import time

import requests

# config
rings = ["a", "b", "c"]
su_per_ring = 3
bake_time = 5

# helper function
def su_info(ring, su_idx):
    service_name = f"ring_{ring}_{su_idx}"
    ring_idx = rings.index(ring) + 1
    port = f"79{ring_idx}{su_idx}"
    tag = f"{ring}{su_idx}"
    return service_name, port, tag

def probe_port(port):
    url = f"http://localhost:{port}/health"
    try:
        r = requests.head(url)
        if r.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

def exec(cmd):
    print(f"> {cmd}")
    os.system(cmd)

if __name__ == "__main__":
    bake_time = int(input("Enter bake time (s): ") or "5")

    # ask about features
    print("Enter the features you want to enable:")
    print("e.g. FEATURE_A=10 / empty line to finish")
    features = []
    while True:
        feature = input()
        if not feature:
            break
        features.append(feature)

    # build new image with hash new tag
    features_args = [f"--build-arg {feature}" for feature in features]
    features_args = " ".join(features_args)
    exec(f"docker build {features_args} . -t sdp-app") 

    # deploy
    for ring in rings:
        for su_idx in range(1, su_per_ring+1):
            print(f"Deploying {ring} {su_idx}")
            service_name, port, tag = su_info(ring, su_idx)
            # tag image
            exec(f"docker tag sdp-app sdp-app:{tag}") 
            # run it with compose
            exec(f"docker compose stop {service_name}")
            exec(f"docker compose up -d {service_name}") 

            time.sleep(bake_time)
            if not probe_port(port):
                print(f"Failed to deploy {service_name}")
                exit(1)

    print("Deployment successful")
