from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Balance
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from django.db.models import Sum

@login_required
def balance_view(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    deposits = Deposit.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    withdrawals = Withdrawal.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    balance.total_balance = deposits - withdrawals
    balance.save()
    return render(request, 'balance/balance.html', {'balance': balance})