from flask import Response, request
from flask_restful import Resource

from database.models import User


class UsersApi(Resource):
    def get(self):
        buses = User.objects().to_json()
        return Response(buses, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        bus = User(**body).save()
        id = bus.id
        return {'id': str(id)}, 200


class UserApi(Resource):
    def get(self, id):
        bus = User.objects.get(id=id).to_json()
        return Response(bus, mimetype="application/json", status=200)

    def put(self, id):
        body = request.get_json()
        User.objects.get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        User.objects.get(id=id).delete()
        return '', 200
