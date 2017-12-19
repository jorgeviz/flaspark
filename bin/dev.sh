#!/bin/bash

# init Redis
nohup redis-server > redis.log 2>&1 & echo $! > redis.pid
echo "Running Redis: " $(cat redis.pid)

# init celery
nohup celery worker -A app.celery > celery.log 2>&1 & echo $! > celery.pid
echo "Running Celery: " $(cat celery.pid)

# WSGI server
source .envvars
source env/bin/activate
python wsgi.py

# Kill Redis & Celery
kill $(cat redis.pid)
kill $(cat celery.pid)

# Delete PID files
rm *.pid

echo ""
echo "Shutted off correctly!"
