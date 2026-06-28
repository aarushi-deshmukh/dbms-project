"""
Gunicorn configuration for production deployment.
This file can be used with: gunicorn -c gunicorn_config.py backend.wsgi:application
"""

import multiprocessing
import os

# Socket binding
bind = "0.0.0.0:8000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_tmp_dir = "/dev/shm"  # Use shared memory for worker communication
keepalive = 5

# Server mechanics
daemon = False
umask = 0
pidfile = None
tmp_upload_dir = None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "ecommerce-api"

# Server hooks
max_requests = 1000
max_requests_jitter = 50
timeout = 60

# Application
default_proc_name = "ecommerce-api"

# Performance
worker_connections = 1000

# Security
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190
