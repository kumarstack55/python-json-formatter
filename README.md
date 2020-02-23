# python-json-formatter

## requirements

* Python 3

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