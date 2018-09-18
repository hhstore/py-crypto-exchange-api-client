# -*- coding: utf-8 -*-
from .base import BaseSchema
from marshmallow import fields


class BaseTickSchema(BaseSchema):
    """
        Time ：      时间
        High ：      最高价
        Low ：       最低价
        Volume ：    交易量
        Last ：      最新价
    """

    Time = fields.String()
    High = fields.String()
    Low = fields.String()
    Volume = fields.String()
    Last = fields.String()
