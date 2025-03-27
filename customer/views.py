from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
from deposit.models import Deposit
from withdrawal.models import Withdrawal
from loan.models import Loan
from installment_payment.models import InstallmentPayment
from installment_planning.models import InstallmentPlan
from django.db.models import Q

@login_required
def create_customer_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # ارتباط مشتری با کاربر لاگین‌شده
            customer.save()
            return redirect('customer_search')
    else:
        form = CustomerForm()
    return render(request, 'customer/create_customer.html', {'form': form})

@login_required
def customer_search_view(request):
    query = request.GET.get('query', '')
    customers = []
    if query:
        customers = Customer.objects.filter(
            Q(national_id=query) |
            Q(account_number=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    return render(request, 'customer/customer_search.html', {'customers': customers, 'query': query})

@login_required
def customer_detail_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = Deposit.objects.filter(user=customer.user)
    withdrawals = Withdrawal.objects.filter(user=customer.user)
    loans = Loan.objects.filter(user=customer.user)
    installment_payments = InstallmentPayment.objects.filter(user=customer.user)
    installment_plans = InstallmentPlan.objects.filter(user=customer.user)
    return render(request, 'customer/customer_detail.html', {
        'customer': customer,
        'deposits': deposits,
        'withdrawals': withdrawals,
        'loans': loans,
        'installment_payments': installment_payments,
        'installment_plans': installment_plans,
    })