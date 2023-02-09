from .route_method_resolve import resolve
from .config import configure_inject
import json


def lambda_handler(event, context):
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
        print(err)
        raise


configure_inject(lambda_handler)
