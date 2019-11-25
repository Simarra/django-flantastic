from django.contrib.gis import admin

from .models import Bakerie, Vote

# Register your models here.


admin.site.register(Bakerie, admin.GeoModelAdmin)
admin.site.register(Vote)
