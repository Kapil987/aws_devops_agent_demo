# lambda_function.py
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # forced failure
    raise Exception("Intentional failure for DevOps Agent test")
