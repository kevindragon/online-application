# -*- coding: utf-8 -*-

import sys
from app.models import People, PeopleExtra

sys.path.append("../application")

people = People.objects.get(1)

print people