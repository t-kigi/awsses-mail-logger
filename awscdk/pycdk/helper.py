#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml

import aws_cdk as cdk


class CDKHelper:
    def __init__(self, conffile: str):
        with open(conffile) as fh:
            self.conf = yaml.safe_load(fh)['CDKConfig']
        self.prefix = self.conf.get('Prefix', '')
        self.suffix = self.conf.get('Suffix', '')

    def sname(self, s: str) -> str:
        """ スタック名を動的に生成します """
        return f'{s}{self.suffix}'

    def rname(self, s: str) -> str:
        """ リソース名を動的に生成します """
        return f'{self.prefix}{s}{self.suffix}'

    def removal_policy(self) -> bool:
        if self.conf.get('RetainWhenDeleted'):
            return cdk.RemovalPolicy.RETAIN
        return cdk.RemovalPolicy.DESTROY
