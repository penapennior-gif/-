from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import AccessCode

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
           
            return redirect('index')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        request.session['special_access_granted'] = False
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            access_code = form.cleaned_data.get('access_code')
            if access_code:
                access_code = access_code.strip()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if access_code:
                    if AccessCode.objects.filter(code=access_code, is_active=True).filter(Q(user__isnull=True) | Q(user=user)).exists():
                        request.session['special_access_granted'] = True
                    else:
                        messages.warning(request, 'Код доступа неверный или не относится к этому пользователю; доступ к корзине и оформлению заявок не предоставлен.')
                return redirect('index')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
  
    return redirect('login')

def no_access(request):
    return render(request, 'accounts/no_access.html')

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except:
        from .models import UserProfile
        profile = UserProfile.objects.create(user=request.user)
    
    return render(request, 'accounts/profile.html', {'profile': profile})