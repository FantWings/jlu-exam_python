from sql.model import db
from sqlalchemy.sql import func


class Paper(db.Model):
    __tablename__ = "papers"
    id = db.Column(db.String(64), primary_key=True, comment='试卷号')
    paper_name = db.Column(db.String(64), nullable=True, comment='试卷名称')
    owner = db.Column(db.String(64), nullable=False, comment='试卷所有者')
    submit_ip = db.Column(db.String(15),
                          default='0.0.0.0',
                          comment='提交者IP地址',
                          nullable=False)
    submit_time = db.Column(db.DateTime,
                            server_default=func.now(),
                            comment='提交时间',
                            nullable=False)
    original = db.Column(db.JSON, nullable=False, comment='原试卷数据')
    used_count = db.Column(db.Integer,
                           default=1,
                           nullable=False,
                           comment='该试卷的被使用次数')
