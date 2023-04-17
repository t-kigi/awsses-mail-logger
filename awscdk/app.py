#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import aws_cdk as cdk

from pycdk.stacks import InitStack
from pycdk.helper import CDKHelper


conffile = os.environ.get('CONFIG_FILE', 'config.yaml')
helper = CDKHelper(conffile)

app = cdk.App()
stack = InitStack(
    app, helper.sname('SESMailLoggerInitStack'), helper)

app.synth()
