FROM python:3.7

EXPOSE 5000

WORKDIR /app

ADD config.py /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
ENTRYPOINT [ "python" ]

CMD [ "run.py" ]