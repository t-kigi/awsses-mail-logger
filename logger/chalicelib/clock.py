#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
システム全体で利用するための時刻取得ロジックを定義します。
時刻はTimezoneを持つ aware オブジェクトです。
"""

from datetime import datetime, timezone, timedelta

from typing import Optional


jst = timezone(timedelta(hours=+9), 'JST')
gmt = timezone(timedelta(hours=0), 'GMT')


def utcnow():
    """ 現在時刻をaware UTCで取得します """
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def jstnow():
    """ 現在時刻を aware JST で取得します """
    return utcnow().astimezone(jst)


def gmtnow():
    """ 現在時刻を aware GMT で取得します """
    return utcnow().astimezone(gmt)


def ttl(expire_seconds: int = 86400, now: datetime = None) -> int:
    """
    now から expire_seconds 秒後の時刻を
    DynamoDBのTTLとして利用可能な形式で返します
    """
    now = now if now else utcnow()
    return int((now + timedelta(seconds=expire_seconds)).timestamp())


def timestamp(dt: datetime) -> int:
    """ dt のタイムスタンプ(単位元: 秒)を返します """
    return int(dt.timestamp())


def fromutctimestamp(utcts: float) -> datetime:
    """ utcts を UTC datetime にして返します  """
    dt = datetime.utcfromtimestamp(utcts)
    return dt.replace(tzinfo=timezone.utc)


def iso2datetime(isoformat: str) -> datetime:
    """ ISO format で記載された文字列を aware datetime で返します """
    return datetime.fromisoformat(isoformat)


def to_jst(dt: datetime) -> datetime:
    """ datetime オブジェクトを JST に変換します """
    return dt.astimezone(jst)


def iso2jst(isoformat: str) -> datetime:
    """ ISO format で記載された文字列を aware datetime で返します """
    return to_jst(datetime.fromisoformat(isoformat))


def strptime(s: str, format: str,
             tz: Optional[str] = jst) -> Optional[datetime]:
    """
    文字列 s を format に従って datetime に変換し
    タイムゾーンを tz に合わせます。
    """
    try:
        return datetime.strptime(s, format).replace(tzinfo=tz)
    except Exception:
        return None


def http_datetime(dt: datetime = None) -> str:
    """ datetime を http の datetime で定義されている形式に変換して返します """
    if dt is None:
        dt = utcnow()
    gmtdt = dt.astimezone(gmt)
    return gmtdt.strftime('%a, %d %b %Y %H:%M:%S GMT')
