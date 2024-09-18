python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py

docker build --build-arg FEATURE_B=10 . -t sdp-app
docker run -p 7900:7900 -it sdp-app
docker inspect --format "{{json .State.Health }}" sdp-sdp-app-a-1-1 | jq

docker-compose up
docker-compose ps 

docker compose stop ring_a_3
docker compose up -d ring_a_3

# setting up minikube

https://minikube.sigs.k8s.io/docs/start/
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/


# alternative: setup aks, install az tool

https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt

rg name: sdp-demo
cluster name: sdp-cluster
region:

az login
az aks get-credentials --resource-group sdp-demo --name sdp-cluster

# after clsuter is created

kubectl create namespace sdp
kubectl config set-context --current --namespace=sdp
kubectl apply -f manifest.yaml

*setup ACR*

# push image to acr to make it available

az acr login --name sdpregistrydemo
docker tag sdp-app sdpregistrydemo.azurecr.io/sdp-app:latest
docker push sdpregistrydemo.azurecr.io/sdp-app:latest

# attach ACR to AKS
az aks update --name scp-cluster --resource-group sdp-demo --attach-acr sdpregistrydemo
