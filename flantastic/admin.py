from django.contrib.gis import admin

from .models import Bakerie, Vote

# Register your models here.


class TasteAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'gout', 'apparence',
              'texture', 'commentaire', 'pate']


admin.site.register(Bakerie, admin.GeoModelAdmin)
admin.site.register(Vote)
