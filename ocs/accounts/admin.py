"""
Description: Admin site file
Modified by: Fátima
Modify date:
"""

from django.contrib import admin
from .models import OCSUser
# Register your models hereself.
admin.site.register(OCSUser)
