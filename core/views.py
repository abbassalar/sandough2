from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from balance.models import Balance
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from loan.models import Loan
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # بعد از ورود به داشبورد برو
        else:
            return render(request, 'core/login.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def test_view(request):
    # یه تاریخ ثابت برای تست
    test_date = datetime(2025, 3, 27, 14, 30)  # 2025-03-27 14:30
    return render(request, 'test.html', {'today': test_date})
@login_required
def dashboard_view(request):
    # محاسبه موجودی
    balance, created = Balance.objects.get_or_create(user=request.user)
    deposits = Deposit.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    withdrawals = Withdrawal.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    balance.total_balance = deposits - withdrawals
    balance.save()

    # گرفتن وام‌های فعال
    loans = Loan.objects.filter(user=request.user, is_paid=False)

    return render(request, 'core/dashboard.html', {
        'balance': balance,
        'loans': loans,
    })