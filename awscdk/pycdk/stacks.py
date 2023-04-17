#!/usr/bin/python
# -*- coding: utf-8 -*-

from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    aws_dynamodb as cdk_dynamodb,
    aws_ses as cdk_ses,
    aws_sns as cdk_sns,
)

from pycdk.helper import CDKHelper


class InitStack(cdk.Stack):
    """ Setup AWS Resources """

    mail_table: cdk_dynamodb.Table
    configuration_set: cdk_ses.ConfigurationSet
    topic: cdk_sns.Topic

    def __init__(self, scope: Construct, construct_id: str,
                 helper: CDKHelper, **kwargs) -> None:
        conf = helper.conf
        removal_policy = helper.removal_policy()

        super().__init__(scope, construct_id, **kwargs)

        # Define DynamoDB tables
        table_prefix = conf.get('DynamoDB', {}).get('TablePrefix', '')
        table_prefix = f'{table_prefix}_' if table_prefix else ''
        self.mail_table = cdk_dynamodb.Table(
            self, 'MailLogTable',
            table_name=f'{table_prefix}MailLog',
            partition_key=cdk_dynamodb.Attribute(
                name="key",
                type=cdk_dynamodb.AttributeType.STRING
            ),
            sort_key=cdk_dynamodb.Attribute(
                name="range",
                type=cdk_dynamodb.AttributeType.STRING
            ),
            billing_mode=cdk_dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute='ttl',
            removal_policy=removal_policy
        )
        cdk.CfnOutput(self, 'MailLogTableName',
                      value=self.mail_table.table_name)

        # SES Configuration set and SNS Topic for notification
        self.configuration_set = cdk_ses.ConfigurationSet(
            self, 'ConfigurationSet',
            configuration_set_name=conf.get('SES', {}).get('ConfigurationSetName')  # noqa
        )
        cdk.CfnOutput(self, 'SESConfigurationSetName',
                      value=self.configuration_set.configuration_set_name)

        self.topic = cdk_sns.Topic(
            self, 'MailNotificationTopic',
            topic_name=conf.get('SNS', {}).get('TopicName'))

        cdk.CfnOutput(self, 'Topic',
                      value=self.topic.topic_arn)

        # set events
        events = conf.get('SES', {}).get('LoggingStatuses', [])
        events = [
            s for s in
            [getattr(cdk_ses.EmailSendingEvent, e, None) for e in events]
            if s
        ]
        self.configuration_set.add_event_destination(
            'ToSns',
            destination=cdk_ses.EventDestination.sns_topic(self.topic),
            events=events
        )
