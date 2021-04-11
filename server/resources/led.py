from flask import request
from flask_restful import Resource

from database.models import User
from resources.led_control import LedControl


class LedApi(Resource):
    def post(self):
        token = request.args.get('token')
        pin = int(request.args.get('pin'))
        value = int(request.args.get('value'))

        if token is None or pin is None or value is None:
            return '', 404

        result = User.objects(mac_hash=token)
        if not result:
            return '', 404

        LedControl().setPinValue(pin=pin, value=value)

        return '', 200
