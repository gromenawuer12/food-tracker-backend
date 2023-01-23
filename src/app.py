from .route_method_resolve import resolve
from .config import configure_inject
import json


def lambda_handler(event, context):
    # event elemento general ???
    try:
        paths = {
            r"\/users.*": "users_blueprint",
            r"\/units.*": "create_units_blueprint",
            r"\/products.*": "create_products_blueprint",
            r"\/recipes.*": "create_recipes_recipes",
            r"\/menus.*": "create_menus_blueprint",
            r"\/monthly_menus.*": "create_monthly_menus_blueprint",
            r"\/weekly_menus.*": "create_weekly_menus_blueprint",
            r"\/nutritional_value.*": "create_nutritional_value_blueprint",
        }
        resolved = resolve(paths, event)
        # print(os.getenv('DB_URL'))
        # print(resolved)
        #
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
