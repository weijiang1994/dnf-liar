"""
coding:utf-8
file: __init__.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/12/6 17:46
@desc:
"""
import click
from flask import Flask
from dnf.setting import DevelopmentConfig
from dnf.view.index import index_bp
from dnf.view.normal import normal_bp
from dnf.extensions import *
from dnf.models import *

areas = ['跨一', '跨二', '跨三A', '跨三B', '跨四', '跨五', '跨六', '跨七', '跨八', ]


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    register_extensions(app)
    register_bp(app)
    register_cmd(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bs.init_app(app)
    ck.init_app(app)


def register_bp(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(normal_bp)


def register_cmd(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        init_server_areas()
        db.session.commit()
        click.echo('初始化数据库完成!')


def init_server_areas():
    for area in areas:
        s = ServerArea(name=area)
        db.session.add(s)
