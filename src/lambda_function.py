# lambda_function.py
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # forced failure
    raise Exception("failure for DevOps Agent test1")

    # return {
    #     "statusCode": 200,
    #     "body": "Success"
    # }
