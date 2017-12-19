# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify, g
from flask_cors import CORS
import json
import datetime
import setup
from celery import Celery
#from app.controllers import jobs

# Flask app declaration
app = Flask(__name__)
CORS(app)

# Flask blueprint registration
#app.register_blueprint(job.mod, url_prefix='/job')

# Celery configuration
c_config = {}
c_config['CELERY_BROKER_URL'] = 'redis://{host}:{port}/0'\
                                    .format(host=setup.CELERY_HOST,
                                            port=setup.CELERY_PORT)
c_config['CELERY_RESULT_BACKEND'] = 'redis://{host}:{port}/0'\
                                        .format(host=setup.CELERY_HOST,
                                                port=setup.CELERY_PORT)

# Initialize Celery
celery = Celery(app.name, broker=c_config['CELERY_BROKER_URL'])
celery.conf.update(c_config)


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
    logger.debug("Teardown context")

@app.route('/')
def main():
    return jsonify({
        'service' : 'Flaspark v{}'.format(setup.__version__),
        'author' : 'Jorge Vizcayno',
        'date' : datetime.datetime.utcnow()
    })

@app.route('/sparktask', methods=['POST'])
def sparktask():
    """ Endpoint to post a new testing task
    """
    # Submit Spark job task
    task = spark_job_task.apply_async()
    return jsonify({
                    'task_id':task.id,
                    'status': 'RUNNING',
                    'progress': 0,
                    'msg': 'Processing...'
                    }), 202 


@app.route('/status/<task_id>')
def taskstatus(task_id, methods=['GET']):
    """ Endpoint to consult tasks status
    """
    # Query task status from Result backend
    task = spark_job_task.AsyncResult(task_id)
    # In case of failure build Bad response
    if task.state == 'FAILURE':
        # something went wrong in the background job
        return jsonify({
            'status': task.state,
            'progress': 100,
            'task_id': task.id,
            'msg': str(task.info),  # this is the exception raised
        }), 200
    else:
        # TODO: Verify status from file from states directory
        # TODO: When Completed, append result to data
        return jsonify({
                'task_id':task.id,
                'status': task.state,
                'progress': 100,
                'msg': 'Processing...'
            })

@celery.task(bind=True)
def spark_job_task(self):
    """ Celery task to submit Test Spark Job
    """
    # Fetch Task ID
    task_id = self.request.id
    # Fetch Spark Config Vars
    master_path = setup.SPARK_MASTER
    project_dir = setup.APP_DIR
    jar_path = '{}/jars/py4j-0.10.1.jar'.format(setup.SPARK_HOME)
    spark_code_path =  project_dir + '/app/spark_test.py'
    # Call Spark Submit
    os.system("{}/bin/spark-submit --master {} --jars {} {} {}".format(
        setup.SPARK_HOME, master_path, jar_path, spark_code_path, task_id))
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}

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