from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Withdrawal
from balance.models import Balance
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from django.db.models import Sum

@login_required
def withdrawal_view(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    deposits = Deposit.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    withdrawals = Withdrawal.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    balance.total_balance = deposits - withdrawals
    balance.save()

    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        if amount <= 0:
            return render(request, 'withdrawal/withdrawal.html', {'error': 'مبلغ باید بیشتر از صفر باشد'})
        if amount > balance.total_balance:
            return render(request, 'withdrawal/withdrawal.html', {'error': 'موجودی کافی نیست'})
        Withdrawal.objects.create(user=request.user, amount=amount)
        return render(request, 'withdrawal/success.html')
    return render(request, 'withdrawal/withdrawal.html')