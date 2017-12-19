# Asynchronous Pyspark Framework in Flask

Web application framework with asyncronous Pyspark jobs execution.

## Pre-requirements

Flaspark v0.0.1 tested with:

- Ubuntu 16.04 LTS
- Python 3.4
- Spark 2.0.0
- Redis 2.8.4

(Not guaranteed for other versions).

Create Virtualenv and install Python reqs.

```bash
    #!/usr/bin/env bash
    sudo apt-get -y update

    # Virtualenv installation
    sudo apt-get -y install python3-pip
    sudo pip3 install virtualenv

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
```

Install Redis

```bash
    sudo apt-get install redis-server
```

Install Spark.

```bash
    #!/usr/bin/env bash

    sudo apt-get -y update

    # Install openjdk if needed
    # sudo apt-get purge openjdk*
    # sudo apt-get -y install openjdk-7-jdk

    # Spark installation
    wget http://d3kbcqa49mib13.cloudfront.net/spark-1.3.1-bin-hadoop2.6.tgz -O spark.tgz
    tar -xf spark.tgz
    rm spark.tgz
    sudo mv spark-* ~/spark
```

*Spark Installation Reference* : <https://github.com/sloanahrens/qbox-blog-code>

## Env Vars

- SPARK_MASTER
- SPARK\_MASTER\_HOME
- SPARK\_CLIENT\_HOME
- PYTHON_PATH
- FLASK_APP
- APP_HOST
- APP_PORT
- DEBUG
- LOGGING_LEVEL
- CELERY_BROKER
- CELERY_HOST
- CELERY_PORT

## Deploy

```bash
    # Run Redis Server in background
    redis-server &
    source .envvars
    source env/bin/activate
    # Start Celery
    celery worker -A app.celery --loglevel=INFO --concurrency=1
    # Only For Local
    python wsgi.py
```

### Credits

- [QBOX](https://qbox.io/blog/asynchronous-apache-spark-flask-celery-elasticsearch) 
- [CODEMENTOR](https://www.codementor.io/jadianes/building-a-web-service-with-apache-spark-flask-example-app-part2-du1083854)
- [STACKOVERFLOW](https://stackoverflow.com/questions/32719920/access-to-spark-from-flask-app)