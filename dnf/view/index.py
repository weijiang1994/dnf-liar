"""
coding:utf-8
file: index.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/12/6 18:10
@desc:
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, ValidationError
from dnf.extensions import db
from dnf.models import ServerArea, LiarInfo


class NewLiarForm(FlaskForm):
    username = StringField(u'角色名', render_kw={'placeholder': '请输入骗子角色名,如果不知道可以为空'})
    adventure_name = StringField(u'冒险团名', render_kw={'placeholder': '请输入冒险团角色名,如果不知道可以为空'})
    server_area = SelectField(u'所在跨区',
                              default=0,
                              coerce=int)
    content = CKEditorField(u'描述内容', validators=[DataRequired(message='请输入描述内容,建议包含有图片')],
                            render_kw={'placeholder': '请输入描述骗子行骗行为的内容,最好包含有图片等信息!'})
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(NewLiarForm, self).__init__(*args, **kwargs)
        categories = ServerArea.query.all()
        self.server_area.choices = [(cate.id, cate.name) for cate in categories]

    def validate_username(self, filed):
        if self.adventure_name.data == '' and filed.data == '':
            raise ValidationError('骗子角色名与冒险团名不能都为空!')


index_bp = Blueprint('index', __name__)


@index_bp.route('/')
@index_bp.route('/index/')
@index_bp.route('/all-liars/')
def index():
    liars = LiarInfo.query.order_by(LiarInfo.timestamps.desc()).all()
    return render_template('index.html', liars=liars)


@index_bp.route('/new-liar/', methods=['GET', 'POST'])
def new_liar():
    form = NewLiarForm()
    if form.validate_on_submit():
        username = form.username.data
        ad_name = form.adventure_name.data
        if username == '':
            username = '角色名未知'
        if ad_name == '':
            ad_name = '冒险团名未知'

        server = form.server_area.data
        content = form.content.data
        remote_ip = request.headers.get('X-Real-Ip')
        if remote_ip is None:
            remote_ip = request.remote_addr
        liar = LiarInfo(username=username,
                        adventure_name=ad_name,
                        content=content,
                        server_id=server,
                        add_person=remote_ip)
        db.session.add(liar)
        db.session.commit()
        flash('骗子添加成功!', 'success')
        return redirect(url_for('.index'))
    return render_template('new-liar.html', form=form)


@index_bp.route('/be-lied/<liar_id>/')
def be_lied(liar_id):
    liar = LiarInfo.query.get_or_404(liar_id)
    liar.lie_times += 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(url_for('.index'))


@index_bp.route('/search/')
def search():
    server_area = request.args.get('searchType')
    type2 = request.args.get('searchType2')
    type3 = request.args.get('searchType3')
    keyword = request.args.get('keyword')
    server_db = ServerArea.query.filter_by(name=server_area).first()
    if server_db:
        liar = search_by_arg(server_db, type2, type3, keyword)
        return render_template('search.html', tag=0, liars=liar, server=server_area, type2=type2, type3=type3,
                               keyword=keyword)
    return render_template('search.html', tag=1)


@index_bp.route('/detail/<liar_id>/')
def liar_detail(liar_id):
    liar = LiarInfo.query.get_or_404(liar_id)
    return render_template('detail.html', liar=liar)


def search_by_arg(ser_db, type1, type2, keyword):
    if type1 == '角色名' and type2 == '精确查询':
        liar = LiarInfo.query.filter(LiarInfo.username == keyword, LiarInfo.server_id == ser_db.id).all()
        return liar

    if type1 == '冒险团名' and type2 == '精确查询':
        liar = LiarInfo.query.filter(LiarInfo.adventure_name == keyword, LiarInfo.server_id == ser_db.id).all()
        return liar

    if type1 == '角色名' and type2 == '模糊查询':
        liar = LiarInfo.query.filter(LiarInfo.username.like('%{}%'.format(keyword)),
                                     LiarInfo.server_id == ser_db.id).all()
        return liar

    if type1 == '冒险团名' and type2 == '模糊查询':
        liar = LiarInfo.query.filter(LiarInfo.adventure_name.like('%{}%'.format(keyword)),
                                     LiarInfo.server_id == ser_db.id).all()
        return liar


@index_bp.route('/callback/', methods=['GET', 'POST'])
def callback():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        print(title)
        print(content)
        flash('意见反馈提交成功!', 'success')
        return redirect(url_for('.index'))
    return render_template('callback.html')
