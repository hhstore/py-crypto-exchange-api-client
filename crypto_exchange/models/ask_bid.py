# -*- coding: utf-8 -*-
from .base import BaseSchema
from marshmallow import Schema, fields


class AskBidSchema(Schema):
    """
        Price:  价格
        Volume: 成交量
    """

    Price = fields.String()
    Volume = fields.String()


class AskBidBaseSchema(BaseSchema):
    """
        Bids
        Asks
    """

    Bids = fields.Nested(AskBidSchema, many=True)
    Asks = fields.Nested(AskBidSchema, many=True)
