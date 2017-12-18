# -*- coding: utf-8 -*-
import logging
from flask import Flask, request, jsonify, g, session 
#from app.controllers import jobs
from flask_cors import CORS
import json
import datetime
import setup

# Flask app declaration
app = Flask(__name__)
CORS(app)

# Flask blueprint registration
#app.register_blueprint(job.mod, url_prefix='/job')

# Logger
logger = logging.Logger('flaspark-{}'.format(setup.__version__),
                        level=setup.LOGGING_LEVEL)

@app.before_request
def before_request():
    """ Before request method
    """
    logger.debug("Before Request")

@app.teardown_appcontext
def td_context(error):
    ''' Teardown app context
    '''
    logger.debug("Teardown Method")
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()
        

@app.route('/')
def main():
    return jsonify({
        'service' : 'Flaspark v{}'.format(setup.__version__),
        'author' : 'Jorge Vizcayno',
        'date' : datetime.datetime.utcnow()
    })

@app.errorhandler(404)
def not_found(error):
    """ Not Found Error Handler
    """
    return jsonify({
        "msg": "Incorrect Path",
        "error": 40004
    }), 400

@app.errorhandler(400)
def bad_request(error):
    """ HTTP Error handling
    """
    return jsonify({
        "error": 40000,
        "msg": "Bad Request"
    }), 400


if __name__ == '__main__':
    app.run(host=setup.APP_HOST,
            port=setup.APP_PORT,
            debug=setup.DEBUG)