#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
一部の設定を別のモジュールに読み込ませるための値の受け渡しを行います。
"""

import yaml

from typing import Any

__STORES = {}


def mutation(key: str, value: Any) -> Any:
    """ 値を登録します """
    __STORES[key] = value
    return value


def get(key: str, else_value: Any = None) -> Any:
    """ 登録した値を取得します """
    return __STORES.get(key, else_value)


def conf(key: str, else_value: Any = None) -> Any:
    """ コンフィグで読み込んだ値を取得します """
    return get('__config', {}).get(key, else_value)


def load_config(config_fullpath: str):
    """ コンフィグファイルを読み込みます """
    with open(config_fullpath) as fh:
        conf = yaml.safe_load(fh)
    mutation('__config', conf.get('Config', {}))
