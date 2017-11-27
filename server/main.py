from flask import Flask
from flask_restful import Resource, Api

from .app import Model

app = Flask(__name__)
api = Api(app)



if __name__ == '__main__':
    app.run(debug=True)