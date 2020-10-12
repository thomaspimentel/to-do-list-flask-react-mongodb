# entry point of the flask web-server
"""index file for REST APIs using Flask"""
import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})

import logger  # nopep8
from app import app  # nopep8

# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on
PORT = os.environ.get('PORT')


@app.errorhandler(404)
def page_not_found(error):
    """ Error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    """ Serve static files """
    return send_from_directory('dist', 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    """ Serve static folders """
    filename = path.split('/')[-1]
    dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, filename)


if __name__ == '__main__':
    LOG.info("running environment: %s", os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))
