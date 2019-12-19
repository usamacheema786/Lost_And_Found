FROM python:3.7

EXPOSE 5000

WORKDIR /Lost_And_Found

# ADD config.py /app

COPY ./requirements.txt /Lost_And_Found/requirements.txt

RUN pip install -r requirements.txt

COPY . /Lost_And_Found
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
ENTRYPOINT [ "python" ]

CMD [ "run.py" ]