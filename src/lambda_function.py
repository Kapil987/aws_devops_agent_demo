# lambda_function.py
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # forced failure
    return {
        "statusCode": 200,
        "body": "Success"
    }
