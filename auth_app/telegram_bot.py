from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.core.wsgi import get_wsgi_application
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_auth_project.settings')
django.setup()

from auth_app.models import LoginToken, TelegramUser
from django.utils import timezone
from datetime import timedelta

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
WEBHOOK_URL = 'https://your-domain.com/webhook/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        token = args[0]
        try:
            login_token = LoginToken.objects.get(token=token, created_at__gte=timezone.now() - timedelta(minutes=10))
            TelegramUser.objects.update_or_create(user=login_token.user, defaults={
                'telegram_id': update.effective_user.id,
                'username': update.effective_user.username
            })
            login_token.delete()
            await update.message.reply_text('Авторизация успешна.')
        except:
            await update.message.reply_text('Неверный или истекший токен.')
    else:
        await update.message.reply_text('Токен не предоставлен.')

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))

async def set_webhook():
    await app.bot.set_webhook(WEBHOOK_URL)

if __name__ == '__main__':
    import asyncio
    asyncio.run(set_webhook())
    app.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path='webhook/',
        webhook_url=WEBHOOK_URL,
    )