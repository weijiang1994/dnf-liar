"""
coding:utf-8
file: extensions.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/12/6 17:48
@desc:
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

ck = CKEditor()
db = SQLAlchemy()
bs = Bootstrap()



