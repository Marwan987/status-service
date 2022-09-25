# VMWARE PROJECT to print url status and response time

clone repo
----------

```
git clone https://github.com/Marwan987/status-service
```

Run helm chart
--------------

```
kubectl create ns vmware
helm install status-service status-service --values status-service/values.yaml --debug -n vmware
```

Port-forwarding
---------------

- Expose promtheus to check it locally
```
kubectl port-forward service/status-service-prometheus-server -n vmware 9090:80
```
- open your browser and type http://127.0.0.1:9090

<img width="1109" alt="image" src="https://user-images.githubusercontent.com/26167640/192163661-d6139e94-9503-4e0c-8d9a-a5e6615ddfd7.png">

- Expose app locally to send requests and check response
```
kubectl port-forward service/status-service -n vmware 8000:8000
```
- open another terminal , and type

```
curl http://127.0.0.1:8000
```

