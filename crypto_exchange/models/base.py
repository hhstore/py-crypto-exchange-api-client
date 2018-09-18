# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class BaseSchema(Schema):
    """
        Exchange：   市场编码
        SecrityCode：交易对
    """

    Exchange = fields.String()
    SecrityCode = fields.String()
