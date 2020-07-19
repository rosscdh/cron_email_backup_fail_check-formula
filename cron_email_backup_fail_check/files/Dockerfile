FROM python:3-alpine
WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["cron_email_backup_fail_check.py"]