# coding: utf-8
import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flasgger import Swagger
from flask_cors import CORS
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
db.init_app(app)
api = Api(app)
# swagger
swag = Swagger(app)
# 跨域
cors = CORS(app)

app.config['DEBUG'] = True
app.config['SWAGGER'] = {
    'title': 'Flasgger RESTful',
    'uiversion': 2
}
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# Turn off the flask_sqlalchemy's modification tracker, and use sqlalchemy's.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secretkey"

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
