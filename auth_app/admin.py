from django.contrib import admin
from .models import TelegramUser, LoginToken

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username')

@admin.register(LoginToken)
class LoginTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'telegram_user', 'created_at')
    readonly_fields = ('token', 'created_at')