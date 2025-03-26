from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from deposit.models import Deposit
from withdrawal.models import Withdrawal

@login_required
def reports_view(request):
    deposits = Deposit.objects.filter(user=request.user)
    withdrawals = Withdrawal.objects.filter(user=request.user)
    return render(request, 'reports/reports.html', {
        'deposits': deposits,
        'withdrawals': withdrawals,
    })