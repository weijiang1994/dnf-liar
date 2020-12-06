"""
coding:utf-8
file: models.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/12/6 17:47
@desc:
"""
from dnf.extensions import db
import datetime


class ServerArea(db.Model):
    __tablename__ = 'server_area'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False, index=True)
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now)

    liar = db.relationship('LiarInfo', back_populates='server_area', cascade='all')


class LiarInfo(db.Model):
    __tablename__ = 'liar_info'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), default='', index=True)
    adventure_name = db.Column(db.String(128), default='', index=True)
    content = db.Column(db.TEXT, default='', nullable=False)
    lie_times = db.Column(db.INTEGER, default=1)
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now)
    server_id = db.Column(db.INTEGER, db.ForeignKey('server_area.id'))
    add_person = db.Column(db.String(200), default='')

    server_area = db.relationship('ServerArea', back_populates='liar')
