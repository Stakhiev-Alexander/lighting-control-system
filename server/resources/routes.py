from .user import UserApi
from .led import LedApi


def initialize_routes(api):
    api.add_resource(UserApi, '/api/users/<mac_hash>')
    api.add_resource(LedApi, '/api/setPinValue')
