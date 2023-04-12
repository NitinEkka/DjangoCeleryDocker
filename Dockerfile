FROM python:3.8-slim-buster

WORKDIR /stockmanagement

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y supervisor && apt-get -y install netcat gcc

COPY requirements.txt /stockmanagement/

RUN pip3 install -r requirements.txt

COPY . /stockmanagement/
 
EXPOSE 8000

RUN python manage.py collectstatic --noinput

# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 22 80

# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# RUN sudo supervisorctl


# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inventory_management.wsgi"]
# CMD ["supervisord"]

# CMD ["celery", "-A", "inventory_app", "beat", "-l", "info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]

# COPY ./workerstart /start-celeryworker
# RUN sed -i 's/\r$//g' /start-celeryworker
# RUN chmod +x /start-celeryworker

# COPY ./beatstart /start-celerybeat
# RUN sed -i 's/\r$//g' /start-celerybeat
# RUN chmod +x /start-celerybeat



# RUN ["python3", "manage.py", "runserver"]