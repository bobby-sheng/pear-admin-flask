### 权限管理 :id=authorize

使用装饰器 @authorize时需要注意，该装饰器需要写在	@app.route	之后

```python
@authorize(power: str, log: bool)
```

第一个参数为权限 code

第二个参数为是否生成日志

```python
# 例如
@authorize("admin:power:remove", log=True)
```

在前端中，例如增加，删除按钮，对于没有编辑权限的用户不显示的话，可以使用

 `{% **if** authorize("admin:user:edit") %}`

 `{% endif %}`

例如

```python
	{% if authorize("admin:user:edit") %}
        <button class="pear-btn pear-btn-primary pear-btn-sm" lay-event="edit">
    	<i class="pear-icon pear-icon-edit"></i>
        </button>
    {% endif %}
    {% if authorize("admin:user:remove") %}
        <button class="pear-btn pear-btn-danger pear-btn-sm" lay-event="remove">
        <i class="pear-icon pear-icon-ashbin"></i>
        </button>
    {% endif %}
```

## model序列化 :id=Schema

- sqlalchemy查询的model对象转dict

  
```
 model_to_dicts(Schema, model)
```

Schema 是  序列化类,我把他放在了models文件里，觉得没有必要见一个文件夹叫Schema，也方便看着模型写序列化类

```python
# 例如
class DeptSchema(ma.Schema):  # 序列化类
    deptId = fields.Integer(attribute="id")
    parentId = fields.Integer(attribute="parent_id")
    deptName = fields.Str(attribute="dept_name")
    leader = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    address = fields.Str()
    status = fields.Str()
    sort = fields.Str()
```

>这一部分有问题的话请看marshmallow文档

model写的是查询后的对象

```python
dept = Dept.query.order_by(Dept.sort).all()
```

进行序列化

```python
res = model_to_dicts(Schema=DeptSchema, model=dept)
```

## 构造查询过滤

```python
# 准确查询字段
# 不等于查询字段
# 大于查询字段
# 小于查询字段
# 模糊查询字段(%+xxx+%)
# 左模糊 (% + xxx) 
# 右模糊查询字段(xxx+ %)
# 包含查询字段
#范围查询字段
# 查询
```

## xss过滤

```python
from applications.common.utils.validate import str_escape
details = str_escape(req.get("details"))
```



## 邮件发送

```python
#在.flaskenv中配置邮箱

from applications/common/utils/mail import send_main
send_mail(subject='title', recipients=['123@qq.com'], content='body')
```



## 返回格式

```
from applications/common/utils/http import success_api,fail_api,table_api

# 这是源代码
def success_api(msg: str = "成功"):
    """ 成功响应 默认值”成功“ """
    return jsonify(success=True, msg=msg)


def fail_api(msg: str = "失败"):
    """ 失败响应 默认值“失败” """
    return jsonify(success=False, msg=msg)


def table_api(msg: str = "", count=0, data=None, limit=10):
    """ 动态表格渲染响应 """
        res = {
            'msg': msg,
            'code': 0,
            'data': data,
            'count': count,
            'limit': limit

        }
        return jsonify(res)
```