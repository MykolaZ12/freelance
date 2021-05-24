FROM python:3.9

WORKDIR /app
ADD ./requirements.txt /app/backend/


RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r backend/requirements.txt

ADD ./ /app/backend
