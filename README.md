# Apache Airflow Docker Setup

A comprehensive Apache Airflow setup with Docker, featuring various operator examples, custom configurations, and Node.js integration for data processing workflows.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Node.js and npm (for local development)

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/cs-sree/apache-airflow-docker.git
cd apache-airflow-docker

# Start Airflow with Docker Compose
docker-compose up -d

# Access Airflow Web UI
# Open http://localhost:8080 in your browser
# Default credentials: admin/admin
```

## 📁 Project Structure

```
apache-airflow-docker/
├── 📄 README.md                          # Project documentation
├── 📄 .env                               # Environment variables
├── 📄 Dockerfile                         # Custom Airflow Docker image
├── 📄 docker-compose.yml                 # Docker Compose configuration
├── 📄 requirements.txt                   # Python dependencies
│
├── 📁 config/                            # Airflow configuration
│   └── airflow.cfg                       # Custom Airflow settings (IST timezone, logging)
│
├── 📁 dags/                              # Airflow DAGs directory
│   ├── 📁 bashOperator/                  # Bash operator examples
│   │   ├── bash-no_with.py               # Basic bash commands
│   │   ├── bash_with.py                  # Bash with context managers
│   │   └── bash_with_decos.py            # Bash with task decorators
│   │
│   ├── 📁 pythonOperator/                # Python operator examples
│   │   ├── pythonOperator_without.py     # Basic Python functions
│   │   ├── pythonOperator_with.py        # Python with context managers
│   │   └── pythonOperator_with_decos.py  # Python with task decorators
│   │
│   ├── 📁 branchPythonOperator/           # Conditional workflow examples
│   │   ├── branch_no_with.py             # Basic branching logic
│   │   ├── branch_with.py                # Branching with context
│   │   └── branch_with_decos.py          # Branching with decorators
│   │
│   ├── 📁 latestOperator/                 # Latest only operator examples
│   │   ├── latest_no_with.py             # Basic latest only execution
│   │   ├── latest_with.py                # Latest only with context
│   │   └── latest_with_decos.py          # Latest only with decorators
│   │
│   ├── 📁 triggerOperator/                # DAG triggering examples
│   │   ├── 📁 with/                      # Trigger DAGs with context
│   │   │   ├── trigger_parent_dag.py     # Parent DAG that triggers child
│   │   │   └── trigger_child_dag.py      # Child DAG that gets triggered
│   │   ├── 📁 no-with/                   # Basic trigger examples
│   │   │   └── triggger_no_with.py       # Simple DAG triggering
│   │   └── 📁 docs/                      # Documented trigger examples
│   │       └── trigger_with_docs.py      # Well-documented trigger DAG
│   │
│   ├── 📁 dockerOperator/                 # Docker operator examples
│   │   └── [Docker-based task examples]
│   │
│   └── 📁 usecases/                       # Real-world use cases
│       └── genai_npm_request.py          # GenAI npm job execution
│
├── 📁 logs/                              # Airflow task logs (auto-generated)
│   └── [Task execution logs with UTC timestamps]
│
└── 📁 plugins/                           # Custom Airflow plugins
    └── [Custom operators, hooks, sensors]
```

## 🛠️ Features

### Core Features
- **Apache Airflow 3.0.3**: Latest version with enhanced features
- **Docker Containerization**: Easy deployment and scaling
- **IST Timezone Configuration**: Logs and UI in Indian Standard Time
- **Node.js Integration**: Execute npm commands from Airflow tasks
- **Custom Logging**: Enhanced JSON logging with timezone support
- **Volume Mounting**: Live development with local file changes

### Operator Examples
- **BashOperator**: Shell command execution
- **PythonOperator**: Python function execution
- **BranchPythonOperator**: Conditional workflow branching
- **TriggerDagOperator**: DAG orchestration and triggering
- **DockerOperator**: Containerized task execution
- **Latest Only Operator**: Skip past runs in catch-up scenarios

### Configuration Features
- Custom Airflow configuration with IST timezone
- Enhanced logging with colored output
- SQLite database for development
- LocalExecutor for task execution
- Web UI with custom timezone display

## 🔧 Configuration

### Environment Variables
The setup includes the following key environment variables:

```bash
# Airflow Core Configuration
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__DEFAULT_TIMEZONE=Asia/Kolkata
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=true
AIRFLOW__CORE__LOAD_EXAMPLES=false

# Database Configuration
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////opt/airflow/airflow.db

# Webserver Configuration
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=true

# Timezone Configuration
TZ=Asia/Kolkata
```

### Custom Airflow Configuration
Located in `config/airflow.cfg`:
- IST timezone settings
- Enhanced logging configuration
- Custom log formatting
- Colored console output

## 📊 Use Cases

### GenAI Request Usage DAG
**File**: `dags/usecases/genai_npm_request.py`

A real-world example that:
- Executes npm commands from within Airflow
- Processes GenAI request usage data
- Integrates with external Node.js applications
- Handles network connectivity between containers and host services

```python
# Example DAG structure
dag = DAG(
    dag_id="node_job_with_bash_operator_local",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    description="Run npm command for GenAI usage processing"
)
```

## 🐳 Docker Configuration

### Custom Dockerfile Features
- Based on `apache/airflow:3.0.3`
- Node.js 18.x integration
- Additional system dependencies (zstd, npm)
- Custom Python packages

### Volume Mounts
- `./dags:/opt/airflow/dags`: DAG files
- `./logs:/opt/airflow/logs`: Task logs
- `./config:/opt/airflow/config`: Configuration files
- `./plugins:/opt/airflow/plugins`: Custom plugins

## 🚦 Getting Started

### 1. Development Setup
```bash
# Clone the repository
git clone https://github.com/cs-sree/apache-airflow-docker.git
cd apache-airflow-docker

# Start the services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 2. Access Airflow UI
- URL: http://localhost:8080
- Username: `admin`
- Password: 'Check logs'
- Run `docker-compose up` to see password in terminal logs

### 3. Running DAGs
1. Navigate to the Airflow UI
2. Enable the desired DAG
3. Trigger manually or wait for scheduled execution
4. Monitor job specific logs in the `logs/` directory

### 4. Development Workflow
1. Add new DAGs to the `dags/` directory
2. Restart Airflow if needed: `docker-compose restart`
3. Check logs for any issues: `docker-compose logs`

## 📝 Example DAG Categories

### Basic Examples
- **bash-no_with.py**: Simple bash command execution
- **pythonOperator_without.py**: Basic Python function tasks

### Advanced Examples
- **bash_with_decos.py**: Modern task decorator patterns
- **branch_with_decos.py**: Conditional workflows
- **trigger_parent_dag.py**: DAG orchestration

### Production Use Cases
- **genai_npm_request.py**: Real-world npm integration
- Custom operators in `plugins/` directory

## 🔍 Troubleshooting

### Common Issues
1. **Port 8080 in use**: Change port in docker-compose.yml
2. **Permission issues**: Check file permissions for volumes
3. **DAG not appearing**: Verify DAG syntax and placement
4. **Timezone issues**: Restart container after config changes

### Log Locations
- Task logs: `logs/[dag_id]/[task_id]/[execution_date]/`
- Scheduler logs: `logs/scheduler/`
- Webserver logs: Docker compose logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your DAG examples or improvements
4. Test with the Docker setup
5. Submit a pull request

## 📚 Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## 📄 License

This project is open source and available under the MIT License.

---

**Last Updated**: July 2025  
**Airflow Version**: 3.0.3  
**Docker Compose Version**: Latest