import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_auth_project.settings')
django.setup()


import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from django.conf import settings
from auth_app.models import LoginToken, TelegramUser
from django.utils import timezone
from datetime import timedelta
from asgiref.sync import sync_to_async



TOKEN = '7807806443:AAHyna09DlP2wcaxuuGbaSWGMCVofiUxV70'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args    
    if args:
        token = args[0]
        try:
            login_token = await sync_to_async(LoginToken.objects.get)(
                token=token,
                created_at__gte=timezone.now() - timedelta(minutes=10)
            )
            
            telegram_user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
                telegram_id=update.effective_user.id,
                defaults={'username': update.effective_user.username or f"user_{update.effective_user.id}"}
            )
            
            login_token.telegram_user = telegram_user
            await sync_to_async(login_token.save)()
            
            await update.message.reply_text('Авторизация успешна. Вернитесь на веб-сайт.')
        except LoginToken.DoesNotExist:
            await update.message.reply_text('Неверный или истёкший токен.')
    else:
        await update.message.reply_text('Токен не предоставлен.')

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("ex")