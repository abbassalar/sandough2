from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("ورود با موفقیت!")
        else:
            return HttpResponse("نام کاربری یا رمز عبور اشتباه است!")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponse("ثبت‌نام با موفقیت!")
    return render(request, 'register.html')

def password_reset_view(request):
    return render(request, 'password_reset.html')  # موقتاً فقط صفحه رو نشون می‌ده