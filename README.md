# python-json-formatter

## requirements

* Python 3

## build

```bash
git clone https://github.com/kumarstack55/python-json-formatter.git
cd python-json-formatter

sudo docker build -t python-json-formatter ./
sudo docker run --name python-json-formatter -d -p 80:80 python-json-formatter

curl http://127.0.0.1/
```

## test

```bash
PYTHONPATH=./src pytest -s
```

## Launch application on GKE cluster

```bash
cluster_name=my-cluster
zone=us-central1-a
project=my-project
name=python-json-formatter
tag=v2

gcloud container clusters get-credentials $cluster_name \
  --zone $zone --project $project
docker build -t "gcr.io/${project}/${name}:${tag}" $PWD
gcloud docker -- push gcr.io/${project}/${name}:${tag}

kubectl run ${name} --image=gcr.io/${project}/${name}:${tag} --port=80
kubectl expose deployment "${name}" --type="LoadBalancer"
kubectl get service "${name}" --watch

ipaddr=$(
  kubectl get service -o json \
    | jq -r "
        .items
        | map(select(.metadata.name == \"${name}\"))
        | .[0].status.loadBalancer.ingress[0].ip
      "
)

curl -s http://${ipaddr}/
```