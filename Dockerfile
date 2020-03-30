FROM python:latest

STOPSIGNAL SIGQUIT

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "gunicorn", "--workers", "2", "app:app", "--access-logfile", "-"]