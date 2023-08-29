import json
import sys

import inject

from com.utils.log import Log

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
        resolved = resolve(event)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(resolved),
            'isBase64Encoded': False
        }
    except Exception as err:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        log.error('Error lambda_handler: {0} {1} {2}'.format(ex_type, str(err), ex_traceback))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'description': str(err)
            }),
            'isBase64Encoded': False
        }
