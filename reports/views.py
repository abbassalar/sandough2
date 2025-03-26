from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from loan.models import Loan
from django.db.models import Sum

@login_required
def reports_view(request):
    deposits = Deposit.objects.filter(user=request.user)
    withdrawals = Withdrawal.objects.filter(user=request.user)
    loans = Loan.objects.filter(user=request.user)
    total_deposits = deposits.aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = withdrawals.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'reports/reports.html', {
        'deposits': deposits,
        'withdrawals': withdrawals,
        'loans': loans,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
    })