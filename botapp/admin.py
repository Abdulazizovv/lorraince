from django.contrib import admin
from botapp.models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    """
    Admin interface for BotUser model.
    """
    list_display = ('user_id', 'username', 'full_name', 'user_type', 'is_active', 'is_admin', 'created_at', 'updated_at')
    search_fields = ('user_id', 'username', 'full_name')
    list_filter = ('user_type', 'is_active', 'is_admin')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'user_id')

admin.site.register(BotUser, BotUserAdmin)