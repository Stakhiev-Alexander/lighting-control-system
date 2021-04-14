from flask import request
from flask_restful import Resource

from database.models import User
from resources.led_control import LedControl


class LedApi(Resource):
    def get(self):
        print('led get')
        pass


    def put(self):
        print('led put')
        pass


    def post(self):
        token = request.args.get('token')
        pin = int(request.args.get('pin'))
        value = int(request.args.get('value'))
        print(f'Request from {token}')

        if token is None or pin is None or value is None:
            return '', 404

        result = User.objects(mac_hash=token)
        if not result:
            return '', 404

        LedControl().set_pin_value(pin=pin, value=value)

        return '', 200
