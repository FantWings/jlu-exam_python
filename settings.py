import os
from datetime import timedelta


class Config(object):
    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}:{}/{}".format(
        os.getenv('SQL_USER'), os.getenv('SQL_PASS'), os.getenv('SQL_HOST'),
        os.getenv('SQL_PORT'), os.getenv('SQL_BASE'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 禁用ASCII编码
    JSON_AS_ASCII = False

    # 设置SESSION安全密钥
    SECRET_KEY = os.urandom(24)

    # 设置SESSION有效期
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)

    # 开启SQLALCHEMY哆嗦模式
    SQLALCHEMY_ECHO = os.getenv('SQL_ECHO', False)
