# xss过滤
from flask import abort, make_response, jsonify, escape


def str_escape(s: str) -> str:
    """xss过滤，内部采用flask自带的过滤函数。
    与原过滤函数不同的是此过滤函数将在 s 为 None 时返回 None。

    :param s: 要过滤的字符串
    :type s: str
    :return: s 为 None 时返回 None，否则过滤字符串后返回。
    :rtype: str
    """
    if not s:
        return None
    return str(escape(s))


def check_data(schema, data):
    errors = schema.validate(data)
    for k, v in errors.items():
        for i in v:
            # print("{}{}".format(k, i))
            msg = "{}{}".format(k, i)
    if errors:
        abort(make_response(jsonify(result=False, msg=msg), 200))
