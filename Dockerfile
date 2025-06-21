FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get -y install cron

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN chmod 0644 /app/crontab
RUN crontab /app/crontab

RUN touch /var/log/cron.log

CMD ["cron", "-f"]