# -*- coding: utf-8 -*-
from .base import BaseSchema
from marshmallow import fields


class TradeBaseSchema(BaseSchema):
    """
        Time:   时间
        Price:  价格
        Volume: 数量
        Type:   买卖类型
    """

    Time = fields.String()
    Price = fields.String()
    Volume = fields.String()
    Type = fields.String()
