FROM python:slim

WORKDIR /usr/src/app

COPY ./code .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./app.py" ]