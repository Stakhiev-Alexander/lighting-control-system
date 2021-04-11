from flask import Response
from flask_restful import Resource

from database.models import User


class UserApi(Resource):
    def get(self, mac_hash):
        user = User.objects.get(mac_hash=mac_hash).to_json()
        return Response(user, mimetype="application/json", status=200)

    def put(self, mac_hash):
        User(mac_hash=mac_hash).save()
        return '', 200

    def delete(self, mac_hash):
        User(mac_hash=mac_hash).delete()
        return '', 200
