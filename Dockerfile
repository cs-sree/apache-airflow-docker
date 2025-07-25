# Use the official Airflow image as base
FROM apache/airflow:3.0.3

# Switch to root to install packages
USER root

# Install any system-level dependencies including Node.js and zstd
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim curl git \
    nodejs npm \
    zstd libzstd-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

#Copy Airflow configuration
COPY config/airflow.cfg /opt/airflow/airflow.cfg

# Copy DAGs
COPY dags/ /opt/airflow/dags/

# Copy plugins
COPY plugins/ /opt/airflow/plugins/

# Switch to root to create logs directory with proper permissions
USER root
RUN mkdir -p /opt/airflow/logs && chown -R airflow:root /opt/airflow/logs && chmod -R 775 /opt/airflow/logs

# Switch back to airflow user
USER airflow

# Install custom Python packages
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Expose Airflow webserver port
EXPOSE 8080
