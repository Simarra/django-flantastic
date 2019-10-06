from django.contrib.gis import admin

from .models import Bakeries

# Register your models here.

admin.site.register(Bakeries, admin.GeoModelAdmin)
