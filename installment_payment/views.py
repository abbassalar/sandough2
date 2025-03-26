from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InstallmentPayment
from loan.models import Loan

@login_required
def installment_payment_view(request):
    loans = Loan.objects.filter(user=request.user, is_paid=False)
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        amount = request.POST.get('amount')
        loan = Loan.objects.get(id=loan_id, user=request.user)
        InstallmentPayment.objects.create(loan=loan, user=request.user, amount=amount)
        return render(request, 'installment_payment/success.html')
    return render(request, 'installment_payment/installment_payment.html', {'loans': loans})