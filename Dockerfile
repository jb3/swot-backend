FROM python:latest

STOPSIGNAL SIGQUIT

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "2", "app:app", "--access-logfile", "-"]