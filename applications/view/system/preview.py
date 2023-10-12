from flask import Blueprint, render_template, request
from applications.common.curd import get_one_by_id

from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Preview
from applications.models import PreviewLog
from applications.models import Preview_history

from sqlalchemy import desc

from request_tools.jenkins_deploy.jenkins_deploy_images import DeployImage
import json

bp = Blueprint('preview', __name__, url_prefix='/preview')


# 用户管理
@bp.get('/')
@authorize("system:preview:main")
def main():
    return render_template('system/preview/main.html')


# 用户分页查询
@bp.get('/data')
@authorize("system:preview:main")
def data():
    # 获取请求参数
    real_name = str_escape(request.args.get('name', type=str))

    filters = []
    if real_name:
        filters.append(Preview.name.contains(real_name))

    query = db.session.query(
        Preview,
    ).filter(*filters).layui_paginate()
    return table_api(
        data=[{
            'id': preview.id,
            'name': preview.name,
            'CMDBTAG': preview.CMDBTAG,
            'EVENTTITAG': preview.EVENTTITAG,
            'HTTPDTAG': preview.HTTPDTAG,
            'GWAYTAG': preview.GWAYTAG,
            'INET_CLIENTTAG': preview.INET_CLIENTTAG,
            'INET_CLIENT_JAVATAG': preview.INET_CLIENT_JAVATAG,
            'INET_NGPARSERTAG': preview.INET_NGPARSERTAG,
            'INET_PLATFORMTAG': preview.INET_PLATFORMTAG,
            'INET_WORKFLOWTAG': preview.INET_WORKFLOWTAG,
            'JSON_ADAPTORTAG': preview.JSON_ADAPTORTAG,
            'LOGSYSTEMTAG': preview.LOGSYSTEMTAG,
            'NETCTAG': preview.NETCTAG,
            'NETDTAG': preview.NETDTAG,
            'NGINXTAG': preview.NGINXTAG,
            'PIPELINETAG': preview.PIPELINETAG,
            'TRIGGERTAG': preview.TRIGGERTAG,
            'POLICYINSIGHTTAG': preview.POLICYINSIGHTTAG,
            'create_at': preview.create_at,
            'update_at': preview.update_at,
        } for preview in query.items],
        count=query.total)

    # 用户增加


@bp.get('/deploy_log')
@authorize("system:preview:deploy_log", log=True)
def deploy_log():
    previewLog = PreviewLog.query.order_by(desc(PreviewLog.create_at)).all()
    return render_template('system/preview/deploy_log.html', data=previewLog)


@bp.get('/get_images_from')
@authorize("system:preview:get_images_from", log=True)
def get_images_from():
    dict_data = ''
    dict_param = request.args.get('dict')
    if dict_param:
        # 解析为字典对象
        dict_data = json.loads(dict_param)
    return render_template('system/preview/get_images_from.html', preview=dict_data)


@bp.post('/get_images_save')
@authorize("system:preview:get_images_from", log=True)
def get_images_save():
    req_json = request.get_json(force=True)
    name = str_escape(req_json.get('name'))
    CMDBTAG = str_escape(req_json.get('CMDBTAG'))
    EVENTTITAG = str_escape(req_json.get('EVENTTITAG'))
    GWAYTAG = str_escape(req_json.get('GWAYTAG'))
    HTTPDTAG = str_escape(req_json.get('HTTPDTAG'))
    INET_CLIENTTAG = str_escape(req_json.get('INET_CLIENTTAG'))
    INET_CLIENT_JAVATAG = str_escape(req_json.get('INET_CLIENT_JAVATAG'))
    INET_NGPARSERTAG = str_escape(req_json.get('INET_NGPARSERTAG'))
    INET_PLATFORMTAG = str_escape(req_json.get('INET_PLATFORMTAG'))
    INET_WORKFLOWTAG = str_escape(req_json.get('INET_WORKFLOWTAG'))
    JSON_ADAPTORTAG = str_escape(req_json.get('JSON_ADAPTORTAG'))
    LOGSYSTEMTAG = str_escape(req_json.get('LOGSYSTEMTAG'))
    NETCTAG = str_escape(req_json.get('NETCTAG'))
    NETDTAG = str_escape(req_json.get('NETDTAG'))
    NGINXTAG = str_escape(req_json.get('NGINXTAG'))
    PIPELINETAG = str_escape(req_json.get('PIPELINETAG'))
    TRIGGERTAG = str_escape(req_json.get('TRIGGERTAG'))
    POLICYINSIGHTTAG = str_escape(req_json.get('POLICYINSIGHTTAG'))

    if not name:
        return fail_api(msg="客户名称不能为空")
    preview = Preview(
        name=name,
        CMDBTAG=CMDBTAG,
        EVENTTITAG=EVENTTITAG,
        GWAYTAG=GWAYTAG,
        HTTPDTAG=HTTPDTAG,
        INET_CLIENTTAG=INET_CLIENTTAG,
        INET_CLIENT_JAVATAG=INET_CLIENT_JAVATAG,
        INET_NGPARSERTAG=INET_NGPARSERTAG,
        INET_PLATFORMTAG=INET_PLATFORMTAG,
        INET_WORKFLOWTAG=INET_WORKFLOWTAG,
        JSON_ADAPTORTAG=JSON_ADAPTORTAG,
        LOGSYSTEMTAG=LOGSYSTEMTAG,
        NETCTAG=NETCTAG,
        NETDTAG=NETDTAG,
        NGINXTAG=NGINXTAG,
        PIPELINETAG=PIPELINETAG,
        TRIGGERTAG=TRIGGERTAG,
        POLICYINSIGHTTAG=POLICYINSIGHTTAG,

    )
    preview_history = Preview_history(
        name=name,
        CMDBTAG=CMDBTAG,
        EVENTTITAG=EVENTTITAG,
        GWAYTAG=GWAYTAG,
        HTTPDTAG=HTTPDTAG,
        INET_CLIENTTAG=INET_CLIENTTAG,
        INET_CLIENT_JAVATAG=INET_CLIENT_JAVATAG,
        INET_NGPARSERTAG=INET_NGPARSERTAG,
        INET_PLATFORMTAG=INET_PLATFORMTAG,
        INET_WORKFLOWTAG=INET_WORKFLOWTAG,
        JSON_ADAPTORTAG=JSON_ADAPTORTAG,
        LOGSYSTEMTAG=LOGSYSTEMTAG,
        NETCTAG=NETCTAG,
        NETDTAG=NETDTAG,
        NGINXTAG=NGINXTAG,
        PIPELINETAG=PIPELINETAG,
        TRIGGERTAG=TRIGGERTAG,
        POLICYINSIGHTTAG=POLICYINSIGHTTAG,

    )
    db.session.add(preview)
    db.session.commit()
    db.session.add(preview_history)
    db.session.commit()
    return success_api(msg="增加成功")


@bp.get('/add')
@authorize("system:preview:add", log=True)
def add():
    preview = Preview.query.all()
    return render_template('system/preview/add.html', preview=preview)


@bp.post('/save')
@authorize("system:preview:add", log=True)
def save():
    req_json = request.get_json(force=True)
    name = str_escape(req_json.get('name'))
    CMDBTAG = str_escape(req_json.get('CMDBTAG'))
    EVENTTITAG = str_escape(req_json.get('EVENTTITAG'))
    GWAYTAG = str_escape(req_json.get('GWAYTAG'))
    HTTPDTAG = str_escape(req_json.get('HTTPDTAG'))
    INET_CLIENTTAG = str_escape(req_json.get('INET_CLIENTTAG'))
    INET_CLIENT_JAVATAG = str_escape(req_json.get('INET_CLIENT_JAVATAG'))
    INET_NGPARSERTAG = str_escape(req_json.get('INET_NGPARSERTAG'))
    INET_PLATFORMTAG = str_escape(req_json.get('INET_PLATFORMTAG'))
    INET_WORKFLOWTAG = str_escape(req_json.get('INET_WORKFLOWTAG'))
    JSON_ADAPTORTAG = str_escape(req_json.get('JSON_ADAPTORTAG'))
    LOGSYSTEMTAG = str_escape(req_json.get('LOGSYSTEMTAG'))
    NETCTAG = str_escape(req_json.get('NETCTAG'))
    NETDTAG = str_escape(req_json.get('NETDTAG'))
    NGINXTAG = str_escape(req_json.get('NGINXTAG'))
    PIPELINETAG = str_escape(req_json.get('PIPELINETAG'))
    TRIGGERTAG = str_escape(req_json.get('TRIGGERTAG'))
    POLICYINSIGHTTAG = str_escape(req_json.get('POLICYINSIGHTTAG'))

    if not name:
        return fail_api(msg="客户名称不能为空")
    preview = Preview(
        name=name,
        CMDBTAG=CMDBTAG,
        EVENTTITAG=EVENTTITAG,
        GWAYTAG=GWAYTAG,
        HTTPDTAG=HTTPDTAG,
        INET_CLIENTTAG=INET_CLIENTTAG,
        INET_CLIENT_JAVATAG=INET_CLIENT_JAVATAG,
        INET_NGPARSERTAG=INET_NGPARSERTAG,
        INET_PLATFORMTAG=INET_PLATFORMTAG,
        INET_WORKFLOWTAG=INET_WORKFLOWTAG,
        JSON_ADAPTORTAG=JSON_ADAPTORTAG,
        LOGSYSTEMTAG=LOGSYSTEMTAG,
        NETCTAG=NETCTAG,
        NETDTAG=NETDTAG,
        NGINXTAG=NGINXTAG,
        PIPELINETAG=PIPELINETAG,
        TRIGGERTAG=TRIGGERTAG,
        POLICYINSIGHTTAG=POLICYINSIGHTTAG,

    )
    preview_history = Preview_history(
        name=name,
        CMDBTAG=CMDBTAG,
        EVENTTITAG=EVENTTITAG,
        GWAYTAG=GWAYTAG,
        HTTPDTAG=HTTPDTAG,
        INET_CLIENTTAG=INET_CLIENTTAG,
        INET_CLIENT_JAVATAG=INET_CLIENT_JAVATAG,
        INET_NGPARSERTAG=INET_NGPARSERTAG,
        INET_PLATFORMTAG=INET_PLATFORMTAG,
        INET_WORKFLOWTAG=INET_WORKFLOWTAG,
        JSON_ADAPTORTAG=JSON_ADAPTORTAG,
        LOGSYSTEMTAG=LOGSYSTEMTAG,
        NETCTAG=NETCTAG,
        NETDTAG=NETDTAG,
        NGINXTAG=NGINXTAG,
        PIPELINETAG=PIPELINETAG,
        TRIGGERTAG=TRIGGERTAG,
        POLICYINSIGHTTAG=POLICYINSIGHTTAG,

    )
    db.session.add(preview)
    db.session.commit()
    db.session.add(preview_history)
    db.session.commit()

    return success_api(msg="增加成功")


# 删除用户
@bp.delete('/remove/<int:id>')
@authorize("system:preview:remove", log=True)
def delete(id):
    user = Preview.query.filter_by(id=id).first()
    user.preview = []

    res = Preview.query.filter_by(id=id).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


# 角色编辑
@bp.get('/edit/<int:id>')
@authorize("system:preview:edit", log=True)
def edit(id):
    preview = get_one_by_id(model=Preview, id=id)
    return render_template('system/preview/edit.html', preview=preview)



#  编辑用户
@bp.put('/update')
@authorize("system:preview:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = req_json.get("previewId")
    data = {
        "name": str_escape(req_json.get("name")),
        "CMDBTAG": str_escape(req_json.get("CMDBTAG")),
        "EVENTTITAG": str_escape(req_json.get("EVENTTITAG")),
        "GWAYTAG": str_escape(req_json.get("GWAYTAG")),
        "HTTPDTAG": str_escape(req_json.get("HTTPDTAG")),
        "INET_CLIENTTAG": str_escape(req_json.get("INET_CLIENTTAG")),
        "INET_CLIENT_JAVATAG": str_escape(req_json.get("INET_CLIENT_JAVATAG")),
        "INET_NGPARSERTAG": str_escape(req_json.get("INET_NGPARSERTAG")),
        "INET_PLATFORMTAG": str_escape(req_json.get("INET_PLATFORMTAG")),
        "INET_WORKFLOWTAG": str_escape(req_json.get("INET_WORKFLOWTAG")),
        "JSON_ADAPTORTAG": str_escape(req_json.get("JSON_ADAPTORTAG")),
        "LOGSYSTEMTAG": str_escape(req_json.get("LOGSYSTEMTAG")),
        "NETCTAG": str_escape(req_json.get("NETCTAG")),
        "NETDTAG": str_escape(req_json.get("NETDTAG")),
        "NGINXTAG": str_escape(req_json.get("NGINXTAG")),
        "PIPELINETAG": str_escape(req_json.get("PIPELINETAG")),
        "TRIGGERTAG": str_escape(req_json.get("TRIGGERTAG")),
        "POLICYINSIGHTTAG": str_escape(req_json.get("POLICYINSIGHTTAG")),
    }
    preview = Preview.query.filter_by(id=id).update(data)
    db.session.commit()
    preview_history = Preview_history(
        name=str_escape(req_json.get("name")),
        CMDBTAG=str_escape(req_json.get("CMDBTAG")),
        EVENTTITAG=str_escape(req_json.get("EVENTTITAG")),
        GWAYTAG=str_escape(req_json.get("GWAYTAG")),
        HTTPDTAG=str_escape(req_json.get("HTTPDTAG")),
        INET_CLIENTTAG=str_escape(req_json.get("INET_CLIENTTAG")),
        INET_CLIENT_JAVATAG=str_escape(req_json.get("INET_CLIENT_JAVATAG")),
        INET_NGPARSERTAG=str_escape(req_json.get("INET_NGPARSERTAG")),
        INET_PLATFORMTAG=str_escape(req_json.get("INET_PLATFORMTAG")),
        INET_WORKFLOWTAG=str_escape(req_json.get("INET_WORKFLOWTAG")),
        JSON_ADAPTORTAG=str_escape(req_json.get("JSON_ADAPTORTAG")),
        LOGSYSTEMTAG=str_escape(req_json.get("LOGSYSTEMTAG")),
        NETCTAG=str_escape(req_json.get("NETCTAG")),
        NETDTAG=str_escape(req_json.get("NETDTAG")),
        NGINXTAG=str_escape(req_json.get("NGINXTAG")),
        PIPELINETAG=str_escape(req_json.get("PIPELINETAG")),
        TRIGGERTAG=str_escape(req_json.get("TRIGGERTAG")),
        POLICYINSIGHTTAG=str_escape(req_json.get("POLICYINSIGHTTAG")),

    )
    db.session.add(preview_history)
    db.session.commit()

    if not preview:
        return fail_api(msg="更新客户版本失败")
    return success_api(msg="更新客户版本成功")


#  部署全部
@bp.get('/deploy_all/<int:id>')
@authorize("system:preview:deploy_all", log=True)
def deploy_all(id):
    preview = get_one_by_id(model=Preview, id=id)
    return render_template('system/preview/deploy_all.html', preview=preview)


#
@bp.post('/deploy_all_put')
@authorize("system:preview:deploy_all", log=True)
def deploy_all_put():
    req_json = request.get_json(force=True)
    res = DeployImage().deploy_all(req_json.copy())
    deploy_type = "全部部署"
    previewLog = PreviewLog(
        name=str_escape(req_json.get("name")),
        type=deploy_type,
        hostip=str_escape(req_json.get("HostIP")),
        # DATA=f"{req_json}",
    )
    db.session.add(previewLog)
    db.session.commit()
    if res == "ok":
        return success_api(msg=f"{res}执行流水线成功")
    else:
        return success_api(msg=f"{res}执行流水线失败")


#  部署单个
@bp.get('/deploy_one/<int:id>')
@authorize("system:preview:deploy_one", log=True)
def deploy_one(id):
    preview = get_one_by_id(model=Preview, id=id)
    return render_template('system/preview/deploy_one.html', preview=preview)


@bp.post('/deploy_one_put')
@authorize("system:preview:deploy_one", log=True)
def deploy_one_put():
    req_json = request.get_json(force=True)
    module = str_escape(req_json.get('module'))
    image = str_escape(req_json.get('image'))
    if not module:
        return fail_api(msg="组件不能为空")
    if not image:
        return fail_api(msg="镜像不能为空")
    res = DeployImage().deploy_one(req_json.copy())
    deploy_type = "单个部署"
    previewLog = PreviewLog(
        name=str_escape(req_json.get("name")),
        type=deploy_type,
        hostip=str_escape(req_json.get("dev")),
        DATA=f"{str_escape(req_json.get('module'))}: {str_escape(req_json.get('image'))}",
    )
    db.session.add(previewLog)
    db.session.commit()
    if res == "ok":
        return success_api(msg=f"{res}执行流水线成功")
    else:
        return success_api(msg=f"{res}执行流水线失败")
