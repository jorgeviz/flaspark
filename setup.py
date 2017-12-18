# -*- coding: utf-8 -*-
__version__ = '0.0.1'
__author__ = 'Jorge Viz'
__mantainer__ = 'javg44@hotmail.com'
import os

# Logging Vars
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL','WARNING')

# APP Vars
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = os.getenv("APP_PORT", 8000)
DEBUG = True if os.getenv('DEBUG', False) else False
