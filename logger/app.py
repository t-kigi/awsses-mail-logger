#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
アプリケーションのエントリーポイントです。
"""

import os
import json

from chalice import Chalice

from chalicelib import store, clock


app = store.mutation('APP', Chalice(app_name='awsses-logger'))
confpath = os.path.join(
    os.path.dirname(__file__), os.environ['CONFIG_FILE'])
store.load_config(confpath)


# load dynamodb after store initialized
from chalicelib import models  # noqa


def save(r: dict):
    """ SNSでの通知内容を DynamoDB に保存します。 """
    try:
        message_id = r['Sns']['MessageId']
        msg = json.loads(r['Sns']['Message'])
        mail = msg['mail']
        event = msg['eventType']
        dests = mail.get('to') or mail.get('destination', [])
        log = models.MailLogging(
            models.MailLogging.HASH(event),
            models.MailLogging.RANGE(message_id))
        log.destinations = dests
        log.mail = mail
        log.ttl = clock.ttl(store.conf('TTL', 86400 * 90))
        log.save()
    except Exception as e:
        app.log.exception(e)


@app.on_sns_message(topic=store.conf('TopicName'))
def handle_sns_message(event):
    for r in event.to_dict().get('Records', []):
        save(r)
