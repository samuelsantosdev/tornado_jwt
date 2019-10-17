import os
import sys
import logging

logger = logging.getLogger(__name__)

try:

    MS_ALLOW_ORIGIN=os.environ.get('MS_ALLOW_ORIGIN')#['*']
    MS_ALLOW_METHODS=os.environ.get('MS_ALLOW_METHODS')#["POST", "GET", "DELETE", "PUT", "PATCH", "OPTIONS"]
    MS_PORT=os.environ.get('MS_PORT')

    DB_HOST=os.environ.get('DB_HOST')
    DB_PORT=os.environ.get('DB_PORT')
    DB_USER=os.environ.get('DB_USER')
    DB_PASS=os.environ.get('DB_PASS')
    DB_NAME=os.environ.get('DB_NAME')

except (AttributeError, TypeError):
    logger.critical('Environment variables is missing')
    sys.exit(1)