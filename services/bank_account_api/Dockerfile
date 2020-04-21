FROM hnq90/chip_python:0.1.1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .

RUN chmod a+x /usr/src/app/docker-entrypoint.sh

CMD ["gunicorn", "-b", "0.0.0.0:5555", "app:app"]

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
