FROM python:3-alpine

WORKDIR /source

RUN pip3 install jinja2 configobj

COPY src .

CMD [ "python3", "./src/interpreter.py" ]
