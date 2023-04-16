import os

import click
from flask.cli import AppGroup

import datetime

from applications.common.script.newmodular.new import NewViewModular
from applications.extensions import db
from applications.models import User, Role, Dept, Power

admin_cli = AppGroup("admin")

now_time = datetime.datetime.now()
userdata = [
    User(
        id=1,
        username='admin',
        password_hash='pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85',
        create_at=now_time,
        enable=1,
        realname='超级管理',
        remark='要是不能把握时机，就要终身蹭蹬，一事无成！',
        avatar='http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg',
        dept_id=1,
    ),
    User(
        id=2,
        username='test',
        password_hash='pbkdf2:sha256:150000$cRS8bYNh$adb57e64d929863cf159f924f74d0634f1fecc46dba749f1bfaca03da6d2e3ac',
        create_at=now_time,
        enable=1,
        realname='测试',
        remark='要是不能把握时机，就要终身蹭蹬，一事无成！',
        avatar='http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg',
        dept_id=1,
    ),
    User(
        id='3',
        username='wind',
        password_hash='pbkdf2:sha256:150000$skME1obT$6a2c20cd29f89d7d2f21d9e373a7e3445f70ebce3ef1c3a555e42a7d17170b37',
        create_at=now_time,
        enable=1,
        realname='风',
        remark='要是不能把握时机，就要终身蹭蹬，一事无成！',
        avatar='http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg',
        dept_id=7,
    ),
]
roledata = [
    Role(
        id=1,
        code='admin',
        name='管理员',
        enable=1,
        details='管理员',
        sort=1,
        create_time=now_time,
    ),
    Role(
        id=2,
        code='common',
        name='普通用户',
        enable=1,
        details='只有查看，没有增删改权限',
        sort=2,
        create_time=now_time,
    )
]
deptdata = [
    Dept(
        id=1,
        parent_id=0,
        dept_name='总公司',
        sort=1,
        leader='就眠仪式',
        phone='12312345679',
        email='123qq.com',
        status=1,
        remark='这是总公司',
        create_at=now_time
    ),
    Dept(
        id=4,
        parent_id=1,
        dept_name='济南分公司',
        sort=2,
        leader='就眠仪式',
        phone='12312345679',
        email='123qq.com',
        status=1,
        remark='这是济南',
        create_at=now_time

    ),
    Dept(
        id=5,
        parent_id=1,
        dept_name='唐山分公司',
        sort=4,
        leader='mkg',
        phone='12312345679',
        email='123qq.com',
        status=1,
        remark='这是唐山',
        create_at=now_time

    ),
    Dept(
        id=7,
        parent_id=4,
        dept_name='济南分公司开发部',
        sort=5,
        leader='就眠仪式',
        phone='12312345679',
        email='123qq.com',
        status=1,
        remark='测试',
        create_at=now_time

    ),
    Dept(
        id=8,
        parent_id=5,
        dept_name='唐山测试部',
        sort=5,
        leader='mkg',
        phone='12312345679',
        email='123qq.com',
        status=1,
        remark='测试部',
        create_at=now_time

    )
]
powerdata = [
    Power(
        id=1,
        name='系统管理',
        type='0',
        code='',
        url=None,
        open_type=None,
        parent_id='0',
        icon='layui-icon layui-icon-set-fill',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=3,
        name='用户管理',
        type='1',
        code='admin:user:main',
        url='/admin/user/',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon layui-icon layui-icon layui-icon-rate',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=4,
        name='权限管理',
        type='1',
        code='admin:power:main',
        url='/admin/power/',
        open_type='_iframe',
        parent_id='1',
        icon=None,
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=9,
        name='角色管理',
        type='1',
        code='admin:role:main',
        url='/admin/role',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-username',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=12,
        name='系统监控',
        type='1',
        code='admin:monitor:main',
        url='/admin/monitor',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-vercode',
        sort=5,
        create_time=now_time,
        enable=1,

    ), Power(
        id=13,
        name='日志管理',
        type='1',
        code='admin:log:main',
        url='/admin/log',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-read',
        sort=4,
        create_time=now_time,
        enable=1,

    ), Power(
        id=17,
        name='文件管理',
        type='0',
        code='',
        url='',
        open_type='',
        parent_id='0',
        icon='layui-icon layui-icon-camera',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=18,
        name='图片上传',
        type='1',
        code='admin:file:main',
        url='/admin/file',
        open_type='_iframe',
        parent_id='17',
        icon='layui-icon layui-icon-camera',
        sort=5,
        create_time=now_time,
        enable=1,

    ), Power(
        id=21,
        name='权限增加',
        type='2',
        code='admin:power:add',
        url='',
        open_type='',
        parent_id='4',
        icon='layui-icon layui-icon-add-circle',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=22,
        name='用户增加',
        type='2',
        code='admin:user:add',
        url='',
        open_type='',
        parent_id='3',
        icon='layui-icon layui-icon-add-circle',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=23,
        name='用户编辑',
        type='2',
        code='admin:user:edit',
        url='',
        open_type='',
        parent_id='3',
        icon='layui-icon layui-icon-rate',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=24,
        name='用户删除',
        type='2',
        code='admin:user:remove',
        url='',
        open_type='',
        parent_id='3',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=25,
        name='权限编辑',
        type='2',
        code='admin:power:edit',
        url='',
        open_type='',
        parent_id='4',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=26,
        name='用户删除',
        type='2',
        code='admin:power:remove',
        url='',
        open_type='',
        parent_id='4',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=27,
        name='用户增加',
        type='2',
        code='admin:role:add',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=28,
        name='角色编辑',
        type='2',
        code='admin:role:edit',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=29,
        name='角色删除',
        type='2',
        code='admin:role:remove',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=30,
        name='角色授权',
        type='2',
        code='admin:role:power',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=4,
        create_time=now_time,
        enable=1,

    ), Power(
        id=31,
        name='图片增加',
        type='2',
        code='admin:file:add',
        url='',
        open_type='',
        parent_id='18',
        icon='',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=32,
        name='图片删除',
        type='2',
        code='admin:file:delete',
        url='',
        open_type='',
        parent_id='18',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=44,
        name='数据字典',
        type='1',
        code='admin:dict:main',
        url='/admin/dict',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-console',
        sort=6,
        create_time=now_time,
        enable=1,

    ), Power(
        id=45,
        name='字典增加',
        type='2',
        code='admin:dict:add',
        url='',
        open_type='',
        parent_id='44',
        icon='',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=46,
        name='字典修改',
        type='2',
        code='admin:dict:edit',
        url='',
        open_type='',
        parent_id='44',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=47,
        name='字典删除',
        type='2',
        code='admin:dict:remove',
        url='',
        open_type='',
        parent_id='44',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=48,
        name='部门管理',
        type='1',
        code='admin:dept:main',
        url='/dept',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-group',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=49,
        name='部门增加',
        type='2',
        code='admin:dept:add',
        url='',
        open_type='',
        parent_id='48',
        icon='',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=50,
        name='部门编辑',
        type='2',
        code='admin:dept:edit',
        url='',
        open_type='',
        parent_id='48',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=51,
        name='部门删除',
        type='2',
        code='admin:dept:remove',
        url='',
        open_type='',
        parent_id='48',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=52,
        name='定时任务',
        type='0',
        code='',
        url='',
        open_type='',
        parent_id='0',
        icon='layui-icon layui-icon-log',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=53,
        name='任务管理',
        type='1',
        code='admin:task:main',
        url='/admin/task',
        open_type='_iframe',
        parent_id='52',
        icon='layui-icon ',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=54,
        name='任务增加',
        type='2',
        code='admin:task:add',
        url='',
        open_type='',
        parent_id='53',
        icon='layui-icon ',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=55,
        name='任务修改',
        type='2',
        code='admin:task:edit',
        url='',
        open_type='',
        parent_id='53',
        icon='layui-icon ',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=56,
        name='任务删除',
        type='2',
        code='admin:task:remove',
        url='',
        open_type='',
        parent_id='53',
        icon='layui-icon ',
        sort=23,
        create_time=now_time,
        enable=1,

    ), Power(
        id=57,
        name='邮件管理',
        type='1',
        code='admin:mail:main',
        url='/admin/mail',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon ',
        sort=7,
        create_time=now_time,
        enable=1,

    ), Power(
        id=58,
        name='邮件发送',
        type='2',
        code='admin:mail:add',
        url='',
        open_type='',
        parent_id='57',
        icon='layui-icon layui-icon-ok-circle',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=59,
        name='邮件删除',
        type='2',
        code='admin:mail:remove',
        url='',
        open_type='',
        parent_id='57',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    )

]


def add_user_role():
    admin_role = Role.query.filter_by(id=1).first()
    admin_user = User.query.filter_by(id=1).first()
    admin_user.role.append(admin_role)
    test_role = Role.query.filter_by(id=2).first()
    test_user = User.query.filter_by(id=2).first()
    test_user.role.append(test_role)
    db.session.commit()


def add_role_power():
    admin_powers = Power.query.filter(Power.id.in_([1, 3, 4, 9, 12, 13, 17, 18, 44, 48])).all()
    admin_user = Role.query.filter_by(id=2).first()
    for i in admin_powers:
        admin_user.power.append(i)
    db.session.commit()


@admin_cli.command("init")
def init_db():
    db.session.add_all(userdata)
    print("加载系统必须用户数据")
    db.session.add_all(roledata)
    print("加载系统必须角色数据")
    db.session.add_all(deptdata)
    print("加载系统必须部门数据")
    db.session.add_all(powerdata)
    print("加载系统必须权限数据")
    db.session.commit()
    print("基础数据存入")
    add_user_role()
    print("用户角色数据存入")
    add_role_power()
    print("角色权限数据存入")
    print("数据初始化完成,请使用python app.py命令运行")


@admin_cli.command()
@click.option('--type', prompt="请输入类型", help='新增的类型')
@click.option('--name', prompt="请输入新增的名称", help='新增的名称')
def new(type, name):
    if type == 'view':
        if name.count('/') > 1:
            print("目前只支持二级目录，多级目录需要蓝图嵌套，本命令暂不支持，请手动创建")
            quit()
        if type == "view" and os.path.exists(f"applications/view/{name}.py"):
            print(f'已经存在视图模块{name}.py')
            quit()
        NewViewModular(name=name).new_view()
