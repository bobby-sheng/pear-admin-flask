import datetime
from applications.extensions import db


class Preview_history(db.Model):
    __tablename__ = 'admin_preview_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    name = db.Column(db.String(20), comment='客户名称')
    CMDBTAG = db.Column(db.String(255), comment='CMDBTAG')
    EVENTTITAG = db.Column(db.String(20), comment='EVENTTITAG')
    GWAYTAG = db.Column(db.String(20), comment='GWAYTAG')
    HTTPDTAG = db.Column(db.String(20), comment='HTTPDTAG')
    INET_CLIENTTAG = db.Column(db.String(20), comment='INET_CLIENTTAG')
    INET_CLIENT_JAVATAG = db.Column(db.String(20), comment='INET_CLIENT_JAVATAG')
    INET_NGPARSERTAG = db.Column(db.String(20), comment='INET_NGPARSERTAG')
    INET_PLATFORMTAG = db.Column(db.String(20), comment='INET_PLATFORMTAG')
    INET_WORKFLOWTAG = db.Column(db.String(20), comment='INET_WORKFLOWTAG')
    JSON_ADAPTORTAG = db.Column(db.String(20), comment='JSON_ADAPTORTAG')
    LOGSYSTEMTAG = db.Column(db.String(20), comment='LOGSYSTEMTAG')
    NETCTAG = db.Column(db.String(20), comment='NETCTAG')
    NETDTAG = db.Column(db.String(20), comment='NETDTAG')
    NGINXTAG = db.Column(db.String(20), comment='NGINXTAG')
    PIPELINETAG = db.Column(db.String(20), comment='PIPELINETAG')
    TRIGGERTAG = db.Column(db.String(20), comment='TRIGGERTAG')
    POLICYINSIGHTTAG = db.Column(db.String(20), comment='POLICYINSIGHTTAG')

    create_at = db.Column(db.DateTime, default=datetime.datetime.now(), comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now(), comment='创建时间')

