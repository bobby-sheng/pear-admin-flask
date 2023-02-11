from applications.common import curd
from applications.models import pluginSetting
from applications.schemas import pluginSettingOutSchema
from applications.extensions import db

def get(key):
    """
    获取设置数据库中保存的值。

    :param key: 查询的键（最长长度 255）

    :return: value
    """
    query = pluginSetting.query.filter_by(key=key).all()
    data = curd.model_to_dicts(schema=pluginSettingOutSchema, data=query)
    if len(data) == 0:
        return None
    return data[0]['value']

def set(key, value):
    """
    设置数据库的值。

    :param key: 设置的键（最长长度 255）
    :param value: 设置的值（最长长度 65525）

    :return: bool
    """
    if len(pluginSetting.query.filter_by(key=key).all()) != 0:
        d = pluginSetting.query.filter_by(key=key).update({"value": value})
        if d:
            db.session.commit()
            return True 
    else:
        setting = pluginSetting(
            key=key,
            value=value
        )
        r = db.session.add(setting)
        db.session.commit()
        return True
    return False
        