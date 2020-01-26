
- Source Repo: https://github.com/helm/charts/tree/master/stable/airflow

- Start tiller service
```
tiller
```

- Clone chart and install chart
```
git clone https://github.com/helm/charts.git
cd chart/stable/airflow
helm dependency update
```

- Configure values.yaml
  - Set the github repository to your github airflow dags repo
```
git:
    ## url to clone the git repository
    url: https://github.com/securethebox/securethebox-airflow-dags.git
```


- Deploy Helm Chart
```
export HELM_HOST=localhost:441324
helm install --name "airflow" . -f values.yaml
```

- Wait for web server to be ready
```
helm status "airflow"
```

- Port forward
```
kubectl port-forward airflow-web-7c586c59bf-b8rsr  8080:8080
```

- Delete Helm
```
export HELM_HOST=localhost:44134
helm delete  --purge "airflow"
```

- How to reload/update DAG
  - Make change to git repository
```
helm upgrade airflow stable/airflow --set tag=v0.0.2
```

## Tiller and Helm commands
```
helm list --host="localhost:44134"

helm delete quarrelsome-umbrellabird --purge --host="localhost:44134"
```

# delete tiller service
kubectl -n kube-system delete deploy tiller-deploy
helm init --service-account default