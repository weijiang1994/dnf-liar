"""
coding:utf-8
file: setting.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/12/6 18:05
@desc:
"""
import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY')

    DB_USER = os.getenv('DB_USER', 'root')
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PWD = os.getenv('DB_PWD')
    DB_PORT = os.getenv('db_port', 3306)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CKEditor configure
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 350
    CKEDITOR_FILE_UPLOADER = 'index.index'


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/dnf_liar?charset=utf8mb4'.format(BaseConfig.DB_USER,
                                                                                         BaseConfig.DB_PWD,
                                                                                         BaseConfig.DB_HOST)
    REDIS_URL = "redis://localhost"
