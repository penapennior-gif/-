from django.contrib import admin
from .models import UserProfile, AccessCode

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'age', 'service_location', 'hired_date')
    list_filter = ('position', 'hired_date')
    search_fields = ('user__username', 'user__email', 'position', 'service_location')
    fields = ('user', 'photo', 'position', 'age', 'hired_date', 'service_location')


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'user', 'is_active', 'created_at')
    list_filter = ('is_active', 'user')
    search_fields = ('code', 'name', 'description', 'user__username')
    readonly_fields = ('created_at',)
    fields = ('user', 'name', 'code', 'is_active', 'description', 'created_at')

