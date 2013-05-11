# -*- coding: utf-8 -*-

import re
from django.core.exceptions import ValidationError

def id_number_validator(value):
    '''验证身份证是否合法'''
    p1 = re.compile(u'^\d{14}[xX\d]$')
    p2 = re.compile(u'^\d{17}[xX\d]$')
    if not p1.match(str(value)) and not p2.match(str(value)):
        raise ValidationError(u'请填写正确的身份证号码')
