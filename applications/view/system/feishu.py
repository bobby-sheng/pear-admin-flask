from flask import Blueprint, render_template, request

from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.common.utils.http import table_api, fail_api, success_api

from request_tools.other_tools.write_fs.to_run import get_info
from request_tools.other_tools.write_fs.add_jira_for_rid import addJiraData

bp = Blueprint('feishu', __name__, url_prefix='/feishu')


# app = Flask(__name__)
# PER_PAGE = 10

# 用户管理
@bp.get('/')
@authorize("system:feishu:main")
def main():
    return render_template('system/feishu/main.html')


# 用户分页查询
@bp.get('/data')
@authorize("system:feishu:main")
def data():
    feishu_data, total = get_info()
    # return data
    # if not feishu_data:

    return table_api(
        data=[{
            'ctime': feishu["ctime"],
            'summary': feishu["summary"],
            'priority': feishu["priority"],
            'release': feishu["release"],
            'labels': feishu["labels"],
            'assignee': feishu["assignee"],
            'record_id': feishu["record_id"],
        } for feishu in feishu_data],
        count=int(total))


# 角色编辑
@bp.get('/remove/<record_id>')
@authorize("system:feishu:edit", log=True)
def remove(record_id):
    print(record_id)
    try:
        res_msf = addJiraData(record_id).write_feishu()
        issa_id = res_msf.split("：")[1]
        print(res_msf, issa_id)
        return success_api(msg=res_msf, data=issa_id)

    except Exception as e:
        # 捕获异常，并打印错误信息
        print(f"查询数据失败: {e}")
        return fail_api(msg=f"失败请重试！{e}")
