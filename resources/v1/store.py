# coding: utf-8
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required
    def get(self, name):
        """
        retrieve one store info
        ---
        tags:
          - store
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    @jwt_required
    def post(self, name):
        """
        create one store info
        ---
        tags:
          - store
        """
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500

        return store.json(), 201

    @jwt_required
    def delete(self, name):
        """
        delete one store info
        ---
        tags:
          - store
        """
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):

    @jwt_required
    def get(self):
        """
        get stores info
        ---
        tags:
          - store
        """
        return {'stores': [store.json() for store in StoreModel.query.all()]}
