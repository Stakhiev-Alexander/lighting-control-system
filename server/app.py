from flask import Flask
from flask_restful import Api
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from database.db import initialize_db
from resources.routes import initialize_routes

DB_PASSWORD = 'admin'
SERVER_NAME = "192.168.100.9"
PORT = 1337

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_HOST'] = f'mongodb+srv://admin:{DB_PASSWORD}@cluster0.utrbc.mongodb.net/allowed_user?retryWrites=true&w=majority'


initialize_db(app)
initialize_routes(api)

print('Staring server')
http_server = HTTPServer(WSGIContainer(app))
print(f'Listening on port: {PORT}')
http_server.listen(PORT, address=SERVER_NAME)
IOLoop.instance().start()
