from flask import Blueprint, render_template, request
from applications.common.curd import get_one_by_id

from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Preview_history

bp = Blueprint('history', __name__, url_prefix='/history')


# 用户管理
@bp.get('/')
@authorize("system:history:main")
def main():
    return render_template('system/history/main.html')


# 用户分页查询
@bp.get('/data')
@authorize("system:history:main")
def data():
    # 获取请求参数
    real_name = str_escape(request.args.get('name', type=str))

    filters = []
    if real_name:
        filters.append(Preview_history.name.contains(real_name))

    # print(*filters)
    query = db.session.query(
        Preview_history,
    ).filter(*filters).layui_paginate()

    return table_api(
        data=[{
            'id': preview_history.id,
            'name': preview_history.name,
            'CMDBTAG': preview_history.CMDBTAG,
            'EVENTTITAG': preview_history.EVENTTITAG,
            'HTTPDTAG': preview_history.HTTPDTAG,
            'GWAYTAG': preview_history.GWAYTAG,
            'INET_CLIENTTAG': preview_history.INET_CLIENTTAG,
            'INET_CLIENT_JAVATAG': preview_history.INET_CLIENT_JAVATAG,
            'INET_NGPARSERTAG': preview_history.INET_NGPARSERTAG,
            'INET_PLATFORMTAG': preview_history.INET_PLATFORMTAG,
            'INET_WORKFLOWTAG': preview_history.INET_WORKFLOWTAG,
            'JSON_ADAPTORTAG': preview_history.JSON_ADAPTORTAG,
            'LOGSYSTEMTAG': preview_history.LOGSYSTEMTAG,
            'NETCTAG': preview_history.NETCTAG,
            'NETDTAG': preview_history.NETDTAG,
            'NGINXTAG': preview_history.NGINXTAG,
            'PIPELINETAG': preview_history.PIPELINETAG,
            'TRIGGERTAG': preview_history.TRIGGERTAG,
            'POLICYINSIGHTTAG': preview_history.POLICYINSIGHTTAG,
            'create_at': preview_history.create_at,
            'update_at': preview_history.update_at,
        } for preview_history in query.items],
        count=query.total)

    # 用户增加
# 删除用户
@bp.delete('/remove/<int:id>')
@authorize("system:history:remove", log=True)
def delete(id):
    user = Preview_history.query.filter_by(id=id).first()
    user.preview = []

    res = Preview_history.query.filter_by(id=id).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")

    # 用户增加
# 角色编辑
@bp.get('/edit/<int:id>')
@authorize("system:history:edit", log=True)
def edit(id):
    preview = get_one_by_id(model=Preview_history, id=id)
    return render_template('system/history/cat_data.html', preview=preview)


