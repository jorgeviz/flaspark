# -*- coding: utf-8 -*-
__version__ = '0.0.1'
__author__ = 'Jorge Viz'
__mantainer__ = 'javg44@hotmail.com'
import os

# Logging Vars
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL','WARNING')

# APP Vars
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))
DEBUG = True if os.getenv('DEBUG', False) else False
APP_DIR = os.getenv('APP_DIR', '/flaskapp')

# Celery Vars
CELERY_BROKER = os.getenv('CELERY_BROKER', 'redis')
CELERY_HOST = os.getenv("CELERY_HOST", "localhost")
CELERY_PORT = int(os.getenv("CELERY_PORT", 6379))

# Current Validations
if CELERY_BROKER != 'redis':
    raise Exception("Not valid Broker, current version only supports Redis!")

# Spark Vars
SPARK_MASTER = os.getenv('SPARK_MASTER', 'local[2]')
SPARK_HOME = os.getenv('SPARK_HOME', '/srv/spark')