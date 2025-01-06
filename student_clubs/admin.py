from django.contrib import admin
from .models import RedSeaUser, Club, Event
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'fullName', 'is_active', 'is_admin', 'is_student', 'is_club_manager','is_sks_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullName',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullName', 'phone_number', 'password1', 'password2', 'is_student', 'is_club_manager', 'is_sks_admin'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()



admin.site.register(RedSeaUser, UserModelAdmin)
admin.site.register(Club)
admin.site.register(Event)