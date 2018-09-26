# coding: utf-8
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.user import UserModel


class UserRegister(Resource):
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
        """
        regist a user
        ---
        tags:
          - user
        """
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'UserModel created successfully.'}, 201


class UserList(Resource):
    @jwt_required
    def get(self):
        """
        get users info
        ---
        tags:
          - user
        """

        return {'users': [user.json() for user in UserModel.query.all()]}
