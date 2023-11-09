from flask import Blueprint, render_template, request

from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.common.utils.http import table_api, fail_api, success_api
from applications.models import FeiShuStory
from request_tools.other_tools.write_fs.to_run import get_story_info
from applications.extensions import db
from request_tools.other_tools.story_write.story_add_for_jira import StoryaddJiraData


bp = Blueprint('feishu_story', __name__, url_prefix='/feishu_story')


# app = Flask(__name__)
# PER_PAGE = 10

# 用户管理
@bp.get('/')
@authorize("system:feishu_story:main")
def main():
    return render_template('system/feishu_story/main.html')


# 用户分页查询
@bp.get('/data')
@authorize("system:feishu_story:main")
def data():
    # 删除表中的所有数据
    db.session.query(FeiShuStory).delete()

    # # 提交事务
    # db.session.commit()

    # 重新调用api获取飞书数据写入数据库
    feishu_data, total = get_story_info()
    insert_data = []
    for feishu in feishu_data:
        insert_data.append({
            "number": feishu["number"],
            "status": feishu["status"],
            "ctime": str(feishu["ctime"]),
            "summary": feishu["summary"],
            "priority": feishu["priority"],
            "put_name": ''.join(feishu["put_name"]),
            "release": feishu["release"],
            "labels": feishu["labels"],
            "assignee": ''.join(feishu["assignee"]),
            "record_id": feishu["record_id"],
        })
    db.session.bulk_insert_mappings(FeiShuStory, insert_data)
    db.session.commit()

    # 获取请求参数
    summary = str_escape(request.args.get('summary', type=str))
    status = str_escape(request.args.get('status', type=str))
    number = str_escape(request.args.get('number', type=str))

    filters = []
    if summary:
        filters.append(FeiShuStory.summary.contains(summary))
    if status:
        filters.append(FeiShuStory.status.contains(status))
    if number:
        filters.append(FeiShuStory.number.contains(number))
    query = db.session.query(
        FeiShuStory,
    ).filter(*filters).layui_paginate()

    return table_api(
        data=[{
            'number': feishu.number,
            'status': feishu.status,
            'ctime': feishu.ctime,
            'summary': feishu.summary,
            'priority': feishu.priority,
            'put_name': feishu.put_name,
            'release': feishu.release,
            'labels': feishu.labels,
            'assignee': feishu.assignee,
            'record_id': feishu.record_id,
        } for feishu in query.items],
        count=query.total)



# 角色编辑
@bp.get('/remove/<record_id>')
@authorize("system:feishu_story:edit", log=True)
def remove(record_id):
    print(record_id)
    try:
        res_msf = StoryaddJiraData(record_id).write_feishu()
        issa_id = res_msf.split("：")[1]
        print(res_msf, issa_id)
        return success_api(msg=res_msf, data=issa_id)

    except Exception as e:
        # 捕获异常，并打印错误信息
        print(f"查询数据失败: {e}")
        return fail_api(msg=f"失败请重试！{e}")
