from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Message
from core.models import Account, Transaction
from loan.models import Loan
from .forms import CustomerForm
import jdatetime


@login_required
def create_customer_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            print(f"Created customer with ID: {customer.id}")

            # ایجاد حساب جدید با شماره حساب واردشده
            account_number = form.cleaned_data['account_number']
            Account.objects.create(
                customer=customer,
                account_number=account_number,
                account_type='SAVINGS',  # می‌تونی اینو توی فرم از کاربر بگیری
                balance=0.00
            )

            messages.success(request, 'مشتری و حساب با موفقیت ایجاد شد.')
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm()

    return render(request, 'customer/create_customer.html', {'form': form})


@login_required
def customer_search_view(request):
    query = request.GET.get('query', '')
    customers = Customer.objects.filter(phone_number__contains=query) if query else Customer.objects.all()
    return render(request, 'customer/customer_search.html', {'customers': customers, 'query': query})


@login_required
def customer_detail_view(request, customer_id):
    print(f"Received customer_id: {customer_id}")
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, 'مشتری موردنظر یافت نشد.')
        return redirect('customer_search')

    print(f"Type of customer after get: {type(customer)}")
    print(f"Customer value after get: {customer}")

    if not isinstance(customer, Customer):
        print("Error: customer is not a Customer instance!")
        raise ValueError("customer must be a Customer instance")

    print(f"Type of customer before accounts query: {type(customer)}")
    print(f"Customer value before accounts query: {customer}")

    accounts = Account.objects.filter(customer=customer)
    print(f"Accounts retrieved: {accounts}")

    transactions = Transaction.objects.filter(account__customer=customer)
    print(f"Transactions retrieved: {transactions}")

    loans = Loan.objects.filter(customer=customer)
    print(f"Loans retrieved: {loans}")

    transactions_with_jalali = []
    for transaction in transactions:
        transaction.date_jalali = jdatetime.datetime.fromgregorian(datetime=transaction.date).strftime('%Y/%m/%d %H:%M')
        transactions_with_jalali.append(transaction)

    loans_with_jalali = []
    for loan in loans:
        loan.date_issued_jalali = jdatetime.datetime.fromgregorian(datetime=loan.date_issued).strftime('%Y/%m/%d %H:%M')
        loans_with_jalali.append(loan)

    return render(request, 'customer/customer_detail.html', {
        'customer': customer,
        'accounts': accounts,
        'transactions': transactions_with_jalali,
        'loans': loans_with_jalali,
    })


@login_required
def edit_customer_view(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, 'مشتری موردنظر یافت نشد.')
        return redirect('customer_search')

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            customer = form.save()
            # به‌روزرسانی شماره حساب توی مدل Account
            account = Account.objects.filter(customer=customer).first()
            if account:
                account_number = form.cleaned_data['account_number']
                # چک کردن اینکه شماره حساب جدید تکراری نباشه
                if Account.objects.exclude(customer=customer).filter(account_number=account_number).exists():
                    messages.error(request, 'این شماره حساب قبلاً برای مشتری دیگری ثبت شده است.')
                    return render(request, 'customer/edit_customer.html', {'customer': customer, 'form': form})
                account.account_number = account_number
                account.save()
            messages.success(request, 'اطلاعات مشتری و حساب با موفقیت ویرایش شد.')
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
        # پر کردن فیلد account_number با مقدار فعلی
        account = Account.objects.filter(customer=customer).first()
        if account:
            form.initial['account_number'] = account.account_number

    return render(request, 'customer/edit_customer.html', {'customer': customer, 'form': form})


@login_required
def send_message_view(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, 'مشتری موردنظر یافت نشد.')
        return redirect('customer_search')

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(
            customer=customer,
            content=content,
            sent_at=jdatetime.datetime.now()
        )
        messages.success(request, 'پیام با موفقیت ارسال شد.')
        return redirect('customer_detail', customer_id=customer.id)

    return render(request, 'customer/send_message.html', {'customer': customer})