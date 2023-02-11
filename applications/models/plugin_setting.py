from applications.extensions import db


class pluginSetting(db.Model):
    __tablename__ = 'plugin_setting'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="设置项ID")
    key = db.Column(db.String(255), comment="设置键")
    value = db.Column(db.String(65535), comment="设置值")

    