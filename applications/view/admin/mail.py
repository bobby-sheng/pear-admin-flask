from flask import Blueprint, render_template, request, current_app
from flask_login import current_user
from flask_mail import Message

from applications.common.curd import model_to_dicts
from applications.common.helper import ModelFilter
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import xss_escape
from applications.extensions import db, flask_mail
from applications.models import Mail
from applications.schemas import MailOutSchema

admin_mail = Blueprint('adminMail', __name__, url_prefix='/admin/mail')


# 用户管理
@admin_mail.get('/')
@authorize("admin:mail:main", log=True)
def main():
    return render_template('admin/mail/main.html')


#   用户分页查询
@admin_mail.get('/data')
@authorize("admin:mail:main", log=True)
def data():
    # 获取请求参数
    receiver = xss_escape(request.args.get("receiver"))
    subject = xss_escape(request.args.get('subject'))
    content = xss_escape(request.args.get('content'))
    # 查询参数构造
    mf = ModelFilter()
    if receiver:
        mf.contains(field_name="receiver", value=receiver)
    if subject:
        mf.contains(field_name="subject", value=subject)
    if content:
        mf.exact(field_name="content", value=content)
    # orm查询
    # 使用分页获取data需要.items
    mail = Mail.query.filter(mf.get_filter(Mail)).layui_paginate()
    count = mail.total
    # 返回api
    return table_api(data=model_to_dicts(schema=MailOutSchema, data=mail.items), count=count)


# 用户增加
@admin_mail.get('/add')
@authorize("admin:mail:add", log=True)
def add():
    return render_template('admin/mail/add.html')


@admin_mail.post('/save')
@authorize("admin:mail:add", log=True)
def save():
    req_json = request.json
    receiver = xss_escape(req_json.get("receiver"))
    subject = xss_escape(req_json.get('subject'))
    content = xss_escape(req_json.get('content'))
    user_id = current_user.id

    try:
        msg = Message(subject=subject, recipients=receiver.split(";"), body=content)
        flask_mail.send(msg)
    except Exception as e:
        current_app.log_exception(e)
        return fail_api(msg="发送失败，请检查邮件配置或发送人邮箱是否写错")

    mail = Mail(receiver=receiver, subject=subject, content=content, user_id=user_id)

    db.session.add(mail)
    db.session.commit()
    return success_api(msg="增加成功")


# 删除用户
@admin_mail.delete('/remove/<int:id>')
@authorize("admin:mail:remove", log=True)
def delete(id):
    res = Mail.query.filter_by(id=id).delete()
    if not res:
        return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")


# 批量删除
@admin_mail.delete('/batchRemove')
@authorize("admin:mail:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        res = Mail.query.filter_by(id=id).delete()
        if not res:
            return fail_api(msg="批量删除失败")
    db.session.commit()
    return success_api(msg="批量删除成功")
