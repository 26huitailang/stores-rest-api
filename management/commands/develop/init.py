#!/usr/bin/env python
# coding=utf-8
"""
为开发环境生成数据。

4级分别4个机构，每个机构一个用户。
机构名每次是随机的一个城市名，用户是umisen + level，密码都是123123。
机构名格式 name_level
"""
import click
import random

from datetime import datetime, timedelta
from flask.cli import with_appcontext
from database import db

from app import create_app
from models.user import UserModel
from models.store import StoreModel
from models.item import ItemModel

BASE_USERNAME = 'peter'
PASSWORD = '123123'
STORES = [
    {
        'store_name': 'nika',
        'store_id': 1,
        'items': [
            {
                'name': 'shoe',
                'price': 19.9,
            },
            {
                'name': 'shirt',
                'price': 16,
            },
            {
                'name': 'hat',
                'price': 13.3,
            }
        ],
    },
    {
        'store_name': 'adi',
        'store_id': 2,
        'items': [
            {
                'name': 'piano',
                'price': 199.9,
            },
            {
                'name': 'tv',
                'price': 160,
            },
            {
                'name': 'iphone',
                'price': 88,
            }
        ],
    }
]


@click.group()
def cli():
    """ Run develop init data. """
    pass


def _add_user():
    user = UserModel(
        username=BASE_USERNAME,
        password=PASSWORD,
    )
    user.save_to_db()
    return

def _add_stores():
    for store in STORES:
        s = StoreModel(
            name=store['store_name']
        )
        s.save_to_db()
        for item in store['items']:
            i = ItemModel(
                name=item['name'],
                price=item['price'],
                store_id=store['store_id'],
            )
            i.save_to_db()
    return

@click.command()
@with_appcontext
def add_fakers():
    """
    初始化开发环境的数据，机构、用户、设备
    """
    _add_user()
    _add_stores()

    print("初始化完成。")
    print("=> 请使用账号：{}，密码：{} 登录".format(BASE_USERNAME, PASSWORD))
    return None
