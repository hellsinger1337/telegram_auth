from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import LoginToken, TelegramUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'username': request.user.telegramuser.username if hasattr(request.user, 'telegramuser') else request.user.username})
    return redirect('login')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    return redirect('home')

def generate_token(request):
    token = LoginToken.objects.create()
    bot_username = 'subhumanAi_bot'
    return JsonResponse({'url': f'https://t.me/{bot_username}?start={token.token}'})
    
def check_token(request, token):
    try:
        login_token = LoginToken.objects.get(token=token)
        
        if login_token.is_valid():
            telegram_user = login_token.telegram_user

            user, created = User.objects.get_or_create(
                username=telegram_user.username
            )
            if created:
                user.set_unusable_password()
                user.save

            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
    except LoginToken.DoesNotExist:
        return JsonResponse({'status': 'invalid'})
    return JsonResponse({'status': 'invalid'})

@csrf_exempt
def webhook(request):
    from django.conf import settings
    import json
    data = json.loads(request.body)
    if 'message' in data and 'text' in data['message']:
        text = data['message']['text']
        chat_id = data['message']['from']['id']
        username = data['message']['from'].get('username', '')
        if text.startswith('/start'):
            token = text.split()[1] if len(text.split()) > 1 else ''
            try:
                login_token = LoginToken.objects.get(token=token, created_at__gte=timezone.now() - timedelta(minutes=10))
                TelegramUser.objects.update_or_create(user=login_token.user, defaults={'telegram_id': chat_id, 'username': username})
                login_token.delete()
            except:
                pass
    return JsonResponse({'status': 'ok'})