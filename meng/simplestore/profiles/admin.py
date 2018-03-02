from django.contrib import admin
from .models import Profile, Home, Business

class ProfilesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("first_name",)}

admin.site.register(Profile,ProfilesAdmin)
admin.site.register(Home)
admin.site.register(Business)
