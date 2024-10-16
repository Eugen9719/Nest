from django.contrib import admin

from user.models import User, Profile

admin.site.register(User)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')
    raw_id_fields = ('user',)
