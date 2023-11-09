from applications.extensions import db


class FeiShuStory(db.Model):
    __tablename__ = 'admin_feishu_story'
    record_id = db.Column(db.Text(), primary_key=True, comment="record_id")
    number = db.Column(db.Text(), comment="需求编号")
    summary = db.Column(db.Text(), comment="需求描述")
    put_name = db.Column(db.Text(), comment="提出人")
    priority = db.Column(db.Text(), comment="优先级")
    release = db.Column(db.Text(), comment="需求分类")
    labels = db.Column(db.Text(), comment="客户")
    status = db.Column(db.Text(), comment="需求状态")
    assignee = db.Column(db.Text(), comment="负责人")
    ctime = db.Column(db.Text(), comment='提出日期')
