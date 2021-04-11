# import RPi.GPIO as GPIO
# from flask import Flask, render_template, request
# app = Flask(__name__)

# GPIO.setmode(GPIO.BCM)

# # Create a dictionary called pins to store the pin number, name, and pin state:
# pins = {
#    23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW},
#    24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
# }

# # Set each pin as an output and make it low:
# for pin in pins:
#    GPIO.setup(pin, GPIO.OUT)
#    GPIO.output(pin, GPIO.LOW)

# @app.route("/")
# def main():
#    # For each pin, read the pin state and store it in the pins dictionary:
#    for pin in pins:
#       pins[pin]['state'] = GPIO.input(pin)
#    # Put the pin dictionary into the template data dictionary:
#    templateData = {
#       'pins' : pins
#       }
#    # Pass the template data into the template main.html and return it to the user
#    return render_template('main.html', **templateData)

# # The function below is executed when someone requests a URL with the pin number and action in it:
# @app.route("/<changePin>/<action>")
# def action(changePin, action):
#    # Convert the pin from the URL into an integer:
#    changePin = int(changePin)
#    # Get the device name for the pin being changed:
#    deviceName = pins[changePin]['name']
#    # If the action part of the URL is "on," execute the code indented below:
#    if action == "on":
#       # Set the pin high:
#       GPIO.output(changePin, GPIO.HIGH)
#       # Save the status message to be passed into the template:
#       message = "Turned " + deviceName + " on."
#    if action == "off":
#       GPIO.output(changePin, GPIO.LOW)
#       message = "Turned " + deviceName + " off."

#    # For each pin, read the pin state and store it in the pins dictionary:
#    for pin in pins:
#       pins[pin]['state'] = GPIO.input(pin)

#    # Along with the pin dictionary, put the message into the template data dictionary:
#    templateData = {
#       'pins' : pins
#    }

#    return render_template('main.html', **templateData)
# import json
#
# from flask import Flask, jsonify
# from flask import request
# from flask_mongoengine import MongoEngine
#
# app = Flask(__name__)
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'allowed_users',
#     'host': 'localhost',
#     'port': 27017
# }
# db = MongoEngine(app)
#
#
# class User(db.Document):
#     mac_hash = db.StringField(required=True, unique=True)
#
#     def to_json(self):
#         return {"mac_hash": self.mac_hash}
#
#
# SERVER_NAME = "example.ru"
# ADMIN_PASS = 'admin'
# PORT = 80
#
#
# # logging.basicConfig(filename='lights_controller_server.log', level=logging.DEBUG)
#
# @app.route('/allowed_users', methods=['GET'])
# def hello_world():
#     mac_hash = request.args.get('mac_hash')
#     print(mac_hash)
#
#     try:
#         users = User.objects(mac_hash=mac_hash)
#         response = {'users': []}
#         for user in users:
#             response['users'].append(user.to_json())
#         return jsonify(response)
#     except:
#         return jsonify({'error': 'data not found'})
#
#
# @app.route('/allowed_users', methods=['PUT'])
# def add_user():
#     try:
#         record = json.loads(request.data)
#         user = User(mac_hash=record['mac_hash'])
#         user.save()
#         return 200
#     except:
#         return 404
#
#
# @app.route('/allowed_users', methods=['DELETE'])
# def del_user():
#     try:
#         record = json.loads(request.data)
#         user = User(mac_hash=record['mac_hash']).first()
#         user.delete()
#         return 200
#     except:
#         return 404
#
#
# app.run(debug=True, use_debugger=False, use_reloader=False, port=8080)
# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(PORT, address=SERVER_NAME)
# logging.info('Attached to {SERVER_NAME}:{PORT}')
# IOLoop.instance().start()


from flask import Flask
from flask_restful import Api

from database.db import initialize_db
from resources.routes import initialize_routes

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/allowed_users'
}

initialize_db(app)
initialize_routes(api)

app.run()
