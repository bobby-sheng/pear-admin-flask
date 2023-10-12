import datetime
from applications.extensions import db


class PreviewLog(db.Model):
    __tablename__ = 'admin_preview_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    type = db.Column(db.String(20), comment='发布类型')
    name = db.Column(db.String(20), comment='客户名称')
    hostip = db.Column(db.String(20), comment='hostip')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now(), comment='部署时间')
    DATA = db.Column(db.String(255), comment='部署数据')
