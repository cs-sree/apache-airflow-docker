# Apache Airflow Kubernetes Deployment with GitSync

This guide provides step-by-step instructions to deploy Apache Airflow on Kubernetes using Helm with GitSync for DAG synchronization.

## 📋 Prerequisites

- Kubernetes cluster (Docker Desktop, Minikube, or cloud provider)
- Helm 3.x installed
- kubectl configured to access your cluster
- GitHub repository with Airflow DAGs

## 🚀 Quick Setup

### 1. Add Apache Airflow Helm Repository

```bash
# Add the official Apache Airflow Helm repository
helm repo add apache-airflow https://airflow.apache.org

# Update Helm repositories
helm repo update
```

### 2. Install/Upgrade Airflow with GitSync

```bash
# Install or upgrade Airflow with GitSync configuration
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --version 1.18.0 \
  -f my-airflow-helm/airflow-values.yaml \
  --timeout 10m
```

### 3. Expose Airflow Web UI (Optional)

```bash
# Patch the API server service to use NodePort for external access
kubectl patch svc airflow-api-server \
  -n airflow \
  -p '{"spec": {"type": "NodePort", "ports": [{"port": 8080, "nodePort": 30080, "protocol": "TCP", "targetPort": 8080}]}}'
```

## 🔍 Verification Commands

### Check Pod Status
```bash
# Check all pods in airflow namespace
kubectl get pods -n airflow

# Watch pods status in real-time
kubectl get pods -n airflow -w
```

### Verify GitSync Configuration
```bash
# Check DAG processor pod details (should show 3/3 containers with GitSync)
kubectl describe pod -l component=dag-processor -n airflow

# Check GitSync container logs
kubectl logs -l component=dag-processor -n airflow -c git-sync

# Check GitSync init container logs
kubectl logs -l component=dag-processor -n airflow -c git-sync-init
```

### Check DAGs Synchronization
```bash
# List DAG files synced from GitHub
kubectl exec -it $(kubectl get pods -n airflow -l component=dag-processor -o jsonpath='{.items[0].metadata.name}') -n airflow -c dag-processor -- ls -la /opt/airflow/dags/repo/dags

# Check specific DAG file content
kubectl exec -it $(kubectl get pods -n airflow -l component=dag-processor -o jsonpath='{.items[0].metadata.name}') -n airflow -c dag-processor -- head -20 /opt/airflow/dags/repo/dags/usecases/genai_npm_request.py
```

### Monitor DAG Processing
```bash
# Check DAG processor logs for DAG loading
kubectl logs -l component=dag-processor -n airflow -c dag-processor | grep -E "Found|Processing|DAG"

# Check scheduler logs
kubectl logs -l component=scheduler -n airflow -c scheduler
```

## 🌐 Access Airflow UI

### Method 1: Port Forwarding (Recommended for Development)
```bash
# Forward local port 8080 to Airflow webserver
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

# Access UI at: http://localhost:8080
# Default credentials: admin/admin
```

### Method 2: NodePort (If configured)
```bash
# Get the NodePort assigned
kubectl get svc airflow-api-server -n airflow

# Access UI at: http://localhost:30080 (or your cluster IP:30080)
```

## 🛠️ Troubleshooting Commands

### Check All Resources
```bash
# List all resources in airflow namespace
kubectl get all -n airflow

# Check services and endpoints
kubectl get svc,endpoints -n airflow
```

### Check Helm Release
```bash
# List Helm releases
helm list -n airflow

# Check Helm release status
helm status airflow -n airflow

# Get applied values
helm get values airflow -n airflow
```

### Check Events and Logs
```bash
# Check Kubernetes events
kubectl get events -n airflow --sort-by='.lastTimestamp'

# Check specific pod logs
kubectl logs <pod-name> -n airflow -c <container-name>

# Check all containers in a pod
kubectl logs <pod-name> -n airflow --all-containers=true
```

### GitSync Specific Troubleshooting
```bash
# Check GitSync synchronization status
kubectl exec -it $(kubectl get pods -n airflow -l component=dag-processor -o jsonpath='{.items[0].metadata.name}') -n airflow -c git-sync -- ls -la /tmp/git

# Check git sync logs for errors
kubectl logs -l component=dag-processor -n airflow -c git-sync --tail=50

# Verify repository access
kubectl exec -it $(kubectl get pods -n airflow -l component=dag-processor -o jsonpath='{.items[0].metadata.name}') -n airflow -c git-sync -- cat /tmp/git/.git/config
```

## 🔧 Configuration Details

### Key Features Enabled
- **GitSync**: Automatically syncs DAGs from GitHub repository
- **KubernetesExecutor**: Runs tasks in separate Kubernetes pods
- **NodePort Service**: Exposes Airflow UI externally
- **Persistent Logs**: Stores logs in Kubernetes persistent volumes

### Repository Configuration
- **Repository**: `https://github.com/cs-sree/apache-airflow-docker.git`
- **Branch**: `main`
- **SubPath**: `dags`
- **Sync Interval**: 60 seconds

### Access Credentials
- **Username**: `admin`
- **Password**: `admin`

## �️ Database Management

### Access PostgreSQL Database
```bash
# Connect to PostgreSQL database
kubectl exec -it airflow-postgresql-0 -n airflow -- psql -U postgres

# Once connected, you can use PostgreSQL commands:
# \dt                    - List all tables
# \d table_name         - Describe a specific table
# \l                    - List all databases
# \q                    - Quit psql
```

### Common PostgreSQL Queries for Airflow
```sql
-- List all tables in the Airflow database
\dt

-- Check DAG runs
SELECT dag_id, execution_date, state FROM dag_run ORDER BY execution_date DESC LIMIT 10;

-- Check task instances
SELECT dag_id, task_id, execution_date, state FROM task_instance ORDER BY execution_date DESC LIMIT 10;

-- Check Airflow connections
SELECT conn_id, conn_type, host, port FROM connection;

-- Check Airflow variables
SELECT key, val FROM variable;

-- Exit PostgreSQL
\q
```

### Database Connection Details
- **Host**: `airflow-postgresql-0.airflow-postgresql-headless.airflow.svc.cluster.local`
- **Port**: `5432`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: `postgres` (default)

## �🔄 Update DAGs

DAGs are automatically synchronized from the GitHub repository every 60 seconds. To manually trigger a sync:

```bash
# Restart the DAG processor to force immediate sync
kubectl rollout restart deployment airflow-dag-processor -n airflow

# Or delete the DAG processor pod to recreate it
kubectl delete pod -l component=dag-processor -n airflow
```

## 🧹 Cleanup

### Remove Airflow Installation
```bash
# Uninstall Airflow release
helm uninstall airflow -n airflow

# Delete the namespace (optional)
kubectl delete namespace airflow
```

### Remove Helm Repository
```bash
# Remove Apache Airflow repository
helm repo remove apache-airflow
```

## 📚 Useful Resources

- [Apache Airflow Helm Chart Documentation](https://airflow.apache.org/docs/helm-chart/)
- [Airflow Configuration Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
- [GitSync Configuration Options](https://github.com/kubernetes/git-sync)
- [Kubernetes Executor Documentation](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html)

---

**Last Updated**: July 2025  
**Airflow Version**: 3.0.3  
**Helm Chart Version**: 1.18.0