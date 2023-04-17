#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
DynamoDB を抽象化して利用するモデルの定義です。
"""


from pynamodb.models import Model
from pynamodb.attributes import (  # noqa
    UnicodeAttribute,
    NumberAttribute,
    ListAttribute,
    MapAttribute,
)

from chalicelib import clock, store


app = store.get('APP')
PROFILE = store.conf('profile')
conf = store.conf('DynamoDB')
TABLE_PREFIX = conf.get('TablePrefix', '')
REGION = conf.get('Region', 'ap-northeast-1')
ENDPOINT = conf.get('Endpoint')
VERSION = conf.get('Version', '2023-04-17')


class BaseModel(Model):
    """ 共通処理定義用のモデル """
    created = UnicodeAttribute(null=True)
    updated = UnicodeAttribute(null=True)
    version = UnicodeAttribute(null=True)

    def finalize(self, **kwargs):
        """ オブジェクト保存前にアプリケーションレベルで必要な値を注入 """
        if kwargs.get('manual'):
            # manual 指定時は何もしない
            return self
        now = clock.to_jst(kwargs.get('now', clock.utcnow())).isoformat()
        if self.created is None:
            self.created = now
        self.updated = now
        self.version = VERSION
        return self

    def save(self, **kwargs):
        self.finalize(**kwargs)
        super().save(**kwargs)


class MailLogging(BaseModel):
    """ ログレコードの保持 """
    class Meta:
        table_name = f'{TABLE_PREFIX}_MailLog'
        region = REGION
        host = ENDPOINT

    @staticmethod
    def HASH(eventtype: str) -> str:
        return f'MailLogging::{eventtype}'

    @staticmethod
    def RANGE(message_id: str) -> str:
        now = clock.jstnow().strftime('%Y%m%d%H%M%S')
        return f'{now}::{message_id}'

    key = UnicodeAttribute(hash_key=True)
    range = UnicodeAttribute(range_key=True)
    destinations = ListAttribute(null=True)
    mail = MapAttribute(null=True)
    ttl = NumberAttribute(null=True)
