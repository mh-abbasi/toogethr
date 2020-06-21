FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN chmod u+s /bin/ping
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY . /app/