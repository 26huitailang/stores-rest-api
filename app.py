# coding: utf-8
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS
from db import db

from resources.v1.user import UserRegister, UserList
from resources.v1.item import Item, ItemList
from resources.v1.store import Store, StoreList
from resources.v1.auth import Auth, RefreshToken


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    api = Api(app)
    # swagger
    Swagger(app)
    # 跨域
    CORS(app)

    app.config['DEBUG'] = True
    app.config['SWAGGER'] = {
        'title': 'Flasgger RESTful',
        'uiversion': 2
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    # Turn off the flask_sqlalchemy's modification tracker, and use sqlalchemy's.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # setup flask-jwt-extended extension
    app.config['JWT_SECRET_KEY'] = 'b75a5bf1-13e8-4223-9b2a-0600b2794c11'
    JWTManager(app)

    # api.add_resource(Auth, '/auth')
    # api.add_resource(Item, '/item/<string:name>')
    # api.add_resource(ItemList, '/items')
    # api.add_resource(Store, '/store/<string:name>')
    # api.add_resource(StoreList, '/stores')
    # api.add_resource(UserRegister, '/register')
    # api.add_resource(UserList, '/users')
    register_api_v1(api, Auth, '/auth')
    register_api_v1(api, RefreshToken, '/refresh')
    register_api_v1(api, Item, '/item/<string:name>')
    register_api_v1(api, ItemList, '/items')
    register_api_v1(api, Store, '/store/<string:name>')
    register_api_v1(api, StoreList, '/stores')
    register_api_v1(api, UserRegister, '/register')
    register_api_v1(api, UserList, '/users')

    return app


def register_api_v1(api_instance, resource_class, api_url):
    api_instance.add_resource(resource_class, '/api/v1{}'.format(api_url))
    return
