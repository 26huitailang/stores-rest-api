#!/usr/bin/env python
# coding=utf-8

import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)
from werkzeug.security import safe_str_cmp

from models.user import UserModel


class Auth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        args = self.parser.parse_args()
        user = UserModel.find_by_username(args['username'])
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        username = args.get('username', None)
        password = args.get('password', None)
        if not username:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        if not (user and safe_str_cmp(user.password, args['password'])):
            return {"msg": "Bad username or password"}, 401

        # Identity can be any data that is json serializable
        ret = {
            'access_token': create_access_token(identity=username, expires_delta=datetime.timedelta(seconds=30)),
            'refresh_token': create_refresh_token(identity=username, expires_delta=datetime.timedelta(days=1)),
        }

        return ret, 200


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
        return ret, 200
