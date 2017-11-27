from flask import Flask
from flask_restful import Api
from app import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, '/todos/')
api.add_resource(Task, '/todo/<todo_id>/task/')

if __name__ == '__main__':
    app.run(debug=True)
