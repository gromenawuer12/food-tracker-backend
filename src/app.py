import json
import sys

import inject
import jwt

from com.utils.log import Log
from com.resources.token.token_invalid_exception import TokenInvalidException

try:
    from com.route_method_resolve import resolve
except Exception as err:
    print('ERROR -> Route resolver: {0}'.format(err))
    raise
try:
    from com.config import configure_inject
except Exception as err:
    print('ERROR -> Configure inject: {0}'.format(err))
    raise


def lambda_handler(event, context):
    print(context.aws_request_id + ': lambda_handler')
    configure_inject(context.aws_request_id)
    return __manage_lambda(event)


@inject.autoparams('log')
def __manage_lambda(event, log: Log):
    log.debug('manage_lambda')
    try:
        response = resolve(event)
        if response is None:
            return {
                'statusCode': 204,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'isBase64Encoded': False
            }
        else:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response),
                'isBase64Encoded': False
            }
    except TokenInvalidException :
        log.error('Token invalid')
        return {
            'statusCode': 401,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'description': str('Token invalid')
            }),
            'isBase64Encoded': False
        }
    except jwt.exceptions.ExpiredSignatureError :
        log.error('Token timeout')
        return {
            'statusCode': 419,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'description': str('Token timeout')
            }),
            'isBase64Encoded': False
        }
    except Exception as error:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        log.error('Error lambda_handler: {0} {1} {2}'.format(ex_type, str(error), ex_traceback))
        return {
            'statusCode': error.status_code if hasattr(error, 'status_code') else 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'description': str(error.message) if hasattr(error, 'message') else str(error)
            }),
            'isBase64Encoded': False
        }
