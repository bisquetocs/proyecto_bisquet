"""
created by:     Django
description:    This are the settings of the provider app
modify by:      Alberto
modify date:    26/10/18
"""

from django.contrib import admin

from .models import Days, OfficeHours

admin.site.register(Days)
admin.site.register(OfficeHours)
