#!/usr/bin/env python
# coding=utf-8


import click

from . import init


@click.group()
def cli():
    """开发环境工具"""
    pass


cli.add_command(init.add_fakers, name='init')
