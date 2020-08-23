from flask import Flask, logging
from flask.logging import default_handler
from flask_cors import CORS

from apigateway.shared.json_encoder import ImprovedJSONEncoder
from apigateway.shared.logging_handler import LoggingHandler
from apigateway.auth import AuthEndpoint


app = Flask(__name__)
app.config.from_pyfile('../config.py')
oidc = AuthEndpoint(app)
cors = CORS(app)

# LOGGING CONFIG
logger = logging.create_logger(app)
logger.removeHandler(default_handler)
logger.addHandler(LoggingHandler())

import apigateway.consumer
import apigateway.views
