#-*- coding: utf-8 -*-
from app import app
import setup

if __name__ == '__main__':
    app.run(host=setup.APP_HOST,
            port=setup.APP_PORT)
