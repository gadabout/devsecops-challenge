## Kubernetes manifests

Manifests for running the bookings API and its database in a cluster. Each workload keeps
its Deployment and Service in one file.

```
namespace.yaml   bookings namespace
secret.yaml      Database URL, JWT secret and Postgres password
rbac.yaml        Service account and role used by the API pods
api.yaml         Bookings API deployment and service
database.yaml    Postgres deployment and service
```

### Usage

```bash
kubectl apply -f k8s/
```
