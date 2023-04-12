# Start Celery
~/Desktop/Stock Management/inventory_management$ celery -A inventory_app worker --loglevel=DEBUG -B --concurrency=1

# New Celery Start
celery -A inventory_app worker -Q queue --loglevel=DEBUG -B --concurrency=1 --pool=solo --without-gossip --without-mingle

# Start Beat
~/Desktop/Stock Management/inventory_management$ celery -A inventory_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Supervisor .conf file
[program:stockmng]
command=gunicorn --bind 127.0.0.1:8000 inventory_management.wsgi
directory=/home/nitin/Desktop/Stock Management/inventory_management
autostart=true
autorestart=true
stderr_logfile=/var/log/myproject.err.log
stdout_logfile=/var/log/myproject.out.log

# docker run image command
sudo docker run -p 8000:8000 my-django-app

# get docker images
docker images

# start docker
systemctl start docker


# get working containers
docker ps

# check supervisor running process
sudo supervisorctl

# stop supervisor process
sudo supervisorctl stop stockmng


# stop/start supervisor
sudo supervisorctl stop/start stockmng

# Check Post usage
sudo lsof -i -P -n | grep LISTEN

# Port Usage PID
lsof -i :8000

# Kill docker container with PID
sudo kill <pid_id>

# Compose and run 
docker-compose up -d --build

# Stop All running container
docker stop $(docker ps -aq)

# Remove all docker container
docker rm -f $(docker ps -aq)

# See logs
docker-compose logs 'celery-beat'

# Remove all docker images
docker rmi -f $(docker images -aq)

# See Network
docker network ls

# Delete all network
docker network prune

# Create Docker Network
docker network create my-network

# Connect django container to network
docker run --name django-container --network my-network -p 8000:8000 django-image

# Stop Redis server
/etc/init.d/redis-server stop

# Collect static
python3 manage.py collectstatic

# Start Supervisor
/usr/bin/supervisord

# dbname
inventory_app_rocketchatconversation

# get in container
docker exec -it CONTAINER_ID bin/bash

# Stop Nginx
sudo systemctl stop nginx

# Static files
files.zip is for the static file , unzip it. Keep it in the root directory.

# Env
Create a virtual env with requirements.txt
