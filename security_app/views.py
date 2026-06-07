from django.shortcuts import render, redirect
from django.contrib.auth import login,  logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.contrib.auth.models import User

def register_view(request: HttpRequest) -> HttpResponse:
    """logic for register"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
    

def login_view(request: HttpRequest) -> HttpResponse:
    """login logic"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})    
    
    
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """logout logic"""
    logout(request)
    return redirect('login')


def home_view(request: HttpRequest) -> HttpResponse:
    """logic for home page"""
    vulnerable_data = "<script>alert('Атака XSS успішна!')</script>"
    safe_data = escape(vulnerable_data)
    return HttpResponse(f"""
        <h1>Головна сторінка проекту</h1>
        <p><b>Спроба атаки:</b> {vulnerable_data}</p>
        <p><b>Очищені та безпечні дані завдяки escape():</b> {safe_data}</p>
    """)


def secure_orm_view(request: HttpRequest) -> HttpResponse:
    """an example of secure data filtering and parametrised requests"""
    user_id = request.GET.get('id', '1')
    
    user = User.objects.filter(id=user_id).first()
    if user:
        return HttpResponse('Користувача знайдено')
    return HttpResponse('Користувача не знайдено')