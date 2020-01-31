FROM python:3

COPY *.py /app/
COPY requirements.txt /app/
COPY .env.dist /app/.env

RUN mkdir -p /app/commands
COPY commands/ /app/commands/

RUN mkdir /app/data

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install --default-timeout=100 -r requirements.txt

CMD python main.py