#!/usr/bin/env python
# coding=utf-8


import click
from flask.cli import FlaskGroup


from app import create_app
from management.commands.develop import cli as develop


@click.group(cls=FlaskGroup, create_app=create_app)
def flask_cli():
    pass


flask_cli.add_command(develop, name='develop')


if __name__ == '__main__':
    flask_cli()
