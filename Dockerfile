FROM python:3.4

COPY /requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY / /app

RUN cd /app/src && ./manage.py migrate

WORKDIR /app/src

EXPOSE 8000
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
