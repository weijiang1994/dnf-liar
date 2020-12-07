"""
# coding:utf-8
@Time    : 2020/12/07
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : normal.py
@Software: PyCharm
"""
import os

from flask import Blueprint, current_app, send_from_directory, request, url_for
from flask_ckeditor import upload_fail, upload_success

normal_bp = Blueprint('normal', __name__, url_prefix='/normal')


@normal_bp.route('/image/upload/')
def image_upload():
    pass


@normal_bp.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['APP_UPLOAD_PATH']
    return send_from_directory(path, filename)


@normal_bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    import random
    pre = random.randint(1, 10000)
    filename = str(pre) + f.filename
    f.save(os.path.join(current_app.config['APP_UPLOAD_PATH'], filename))
    url = url_for('normal.uploaded_files', filename=filename)
    return upload_success(url=url)
