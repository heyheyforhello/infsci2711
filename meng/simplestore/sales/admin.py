from django.contrib import admin
from .models import Salesperson, Store#, Region
# Register your models here.
# class RegionAdmin(admin.ModelAdmin):
#     model = Region

admin.site.register(Salesperson)
admin.site.register(Store)
# admin.site.register(Region, RegionAdmin)
