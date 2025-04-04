from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Loan, InstallmentPayment
from django.utils import timezone

@login_required
def loan_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        Loan.objects.create(user=request.user, amount=amount)
        return render(request, 'loan/success.html')
    return render(request, 'loan/loan.html')

@login_required
def installment_payment_view(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        # ثبت پرداخت قسط
        InstallmentPayment.objects.create(
            loan=loan,
            amount=amount,
            payment_date=timezone.now()
        )
        messages.success(request, 'پرداخت قسط با موفقیت ثبت شد.')
        return redirect('loan_detail', loan_id=loan.id)
    return render(request, 'loan/installment_payment.html', {'loan': loan})

@login_required
def loan_detail_view(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    payments = InstallmentPayment.objects.filter(loan=loan)
    return render(request, 'loan/loan_detail.html', {
        'loan': loan,
        'payments': payments,
    })