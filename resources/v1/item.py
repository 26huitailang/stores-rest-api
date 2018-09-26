# coding: utf-8
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,  # can't through without 'price'
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,  # can't through without 'price'
        help="This field cannot be left blank!"
    )

    @jwt_required
    def get(self, name):
        """
        获取一个item
        ---
        tags:
          - item
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required
    def post(self, name):
        """
        create one item
        ---
        tags:
          - item
        """
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500  # Internal Server error

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        """
        delete one item
        ---
        tags:
          - item
        """
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    @jwt_required
    def put(self, name):
        """
        update one item
        ---
        tags:
          - item
        """
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {'message': "An error occurred inserting the item."}, 500  # Internal Server error
        else:
            try:
                item.price = data['price']
            except:
                return {'message': "An error occurred updating the item."}, 500  # Internal Server error
        return item.json()


class ItemList(Resource):
    @jwt_required
    def get(self):
        """
        item list
        ---
        tags:
          - item
        responses:
          200:
            description: The task data
            schema:
              id: Item
              properties:
                items:
                  type: list
                  default: []
        """
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
