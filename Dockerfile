FROM python:3.7

COPY . /root
COPY requirements.txt /root

WORKDIR /root

RUN pip install -r requirements.txt
CMD mkdir cache/
# CMD source bots/bin/activate