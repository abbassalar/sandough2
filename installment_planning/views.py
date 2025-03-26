from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InstallmentPlan
from loan.models import Loan
from django.utils import timezone

@login_required
def installment_planning_view(request):
    loans = Loan.objects.filter(user=request.user, is_paid=False)
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        number_of_installments = request.POST.get('number_of_installments')
        amount_per_installment = request.POST.get('amount_per_installment')
        loan = Loan.objects.get(id=loan_id, user=request.user)
        InstallmentPlan.objects.create(
            loan=loan,
            user=request.user,
            number_of_installments=number_of_installments,
            amount_per_installment=amount_per_installment,
            start_date=timezone.now()
        )
        return render(request, 'installment_planning/success.html')
    return render(request, 'installment_planning/installment_planning.html', {'loans': loans})