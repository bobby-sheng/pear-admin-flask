from flask import Blueprint, render_template, request

from applications.common.utils.rights import authorize
import json
import yaml
import jsonpath

bp = Blueprint('json_to_yaml', __name__, url_prefix='/json_to_yaml')


# app = Flask(__name__)
# PER_PAGE = 10

# 用户管理
@bp.get('/')
@authorize("system:json_to_yaml:main")
def main():
    return render_template('system/json_to_yaml/main.html')


@bp.route('/convert', methods=['POST'])
@authorize("system:json_to_yaml:main")
def convert():
    json_data = request.form['json']
    try:
        data = json.loads(json_data)
        if isinstance(data, str):
            data = eval(data)
        yaml_data = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return yaml_data
    except Exception as e:
        return str(e)


@bp.route('/jsonpath_to', methods=['POST'])
@authorize("system:json_to_yaml:main")
def jsonpath_to():
    json_data = request.form['json']
    json_path = request.form['json_path']
    try:
        data = json.loads(json_data)
        if isinstance(data, str):
            data = eval(data)
        jsonpata_data = jsonpath.jsonpath(data, json_path)
        return str(jsonpata_data)
    except Exception as e:
        return str(e)
