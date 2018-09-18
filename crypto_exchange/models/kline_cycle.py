# -*- coding: utf-8 -*-
from .base import BaseSchema
from marshmallow import fields


class KlineCycleBaseSchema(BaseSchema):
    """
        CycleType    int32  `json:"CycleType"`
        Time         string `json:"Time"`
        Open         string `json:"Open"`
        High         string `json:"High"`
        Low          string `json:"Low"`
        Close        string `json:"Close"`
        Amount       string `json:"Amount"`
        Volume       string `json:"Volume"`
    """

    CycleType = fields.Integer()
    Time = fields.String()
    Open = fields.String()
    High = fields.String()
    Low = fields.String()
    Close = fields.String()
    Amount = fields.String()
    Volume = fields.String()
