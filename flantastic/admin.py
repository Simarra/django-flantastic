from django.contrib.gis import admin

from .models import Bakeries, Taste_choice

# Register your models here.


class TasteAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'rate']


admin.site.register(Bakeries, admin.GeoModelAdmin)
admin.site.register(Taste_choice)
