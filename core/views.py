from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from customer.models import Customer
from core.models import Account, Transaction, Notification, UserProfile
from loan.models import Loan
from balance.models import Balance
import jdatetime
from django.utils.timezone import now
import re
from datetime import datetime


def persian_to_latin_digits(text):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    latin_digits = "0123456789"
    translation_table = str.maketrans(persian_digits, latin_digits)
    return text.translate(translation_table)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'نام کاربری قبلاً استفاده شده است.')
            return render(request, 'core/register.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'ثبت‌نام با موفقیت انجام شد. لطفاً وارد شوید.')
        return redirect('login')
    return render(request, 'core/register.html')


@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        profile.phone_number = request.POST['phone_number']
        profile.national_code = request.POST['national_code']
        profile.address = request.POST['address']
        try:
            profile.save()
            messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد.')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'خطا در به‌روزرسانی پروفایل: {str(e)}')

    return render(request, 'core/edit_profile.html', {'profile': profile})


@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        customers = Customer.objects.all()
        loans = Loan.objects.all()
        accounts = Account.objects.all()
        transactions = Transaction.objects.all()
        notifications = Notification.objects.all()
        balance = None
    else:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            return redirect('create_customer')
        customers = [customer]
        loans = Loan.objects.filter(customer=customer)
        accounts = Account.objects.filter(customer=customer)
        transactions = Transaction.objects.filter(account__customer=customer)
        notifications = Notification.objects.filter(user=request.user)
        balance = Balance.objects.filter(customer=customer).first()

    # تبدیل تاریخ‌ها به شمسی
    for transaction in transactions:
        transaction.date_shamsi = jdatetime.datetime.fromgregorian(datetime=transaction.date).strftime('%Y/%m/%d %H:%M')
    for notification in notifications:
        notification.created_at_shamsi = jdatetime.datetime.fromgregorian(datetime=notification.created_at).strftime(
            '%Y/%m/%d %H:%M')

    context = {
        'customers': customers,
        'loans': loans,
        'accounts': accounts,
        'transactions': transactions,
        'notifications': notifications,
        'balance': balance,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def create_customer_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        national_id = request.POST.get('national_id', '').strip()
        id_number = request.POST.get('id_number', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        birth_date_gregorian = request.POST.get('birth_date_gregorian', None)
        gender = request.POST.get('gender', None)
        customer_type = request.POST.get('customer_type', None)
        address = request.POST.get('address', '').strip()
        id_copy = request.FILES.get('id_copy', None)

        # اعتبارسنجی‌ها
        is_valid = True

        # نام
        if not first_name:
            messages.error(request, 'نام اجباری است.')
            is_valid = False

        # نام خانوادگی
        if not last_name:
            messages.error(request, 'نام خانوادگی اجباری است.')
            is_valid = False

        # کد ملی
        def validate_national_id(nid):
            if not re.match(r'^\d{10}$', nid):
                return False
            check = int(nid[9])
            sum = 0
            for i in range(9):
                sum += int(nid[i]) * (10 - i)
            remainder = sum % 11
            return (remainder < 2 and check == remainder) or (remainder >= 2 and check == 11 - remainder)

        if not validate_national_id(national_id):
            messages.error(request, 'کد ملی نامعتبر است.')
            is_valid = False

        # شماره شناسنامه
        if not re.match(r'^\d{1,20}$', id_number):
            messages.error(request, 'شماره شناسنامه باید فقط شامل اعداد باشد (حداکثر 20 رقم).')
            is_valid = False

        # شماره تلفن
        if not re.match(r'^09\d{9}$', phone_number):
            messages.error(request, 'شماره تلفن باید با 09 شروع شود و 11 رقم باشد.')
            is_valid = False

        # ایمیل
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, 'ایمیل نامعتبر است.')
            is_valid = False

        # تاریخ تولد
        birth_date = None
        if birth_date_gregorian:
            try:
                # دیباگ: چاپ مقدار birth_date_gregorian
                print(f"birth_date_gregorian: {birth_date_gregorian}")
                # تبدیل اعداد فارسی به لاتین
                birth_date_gregorian = persian_to_latin_digits(birth_date_gregorian)
                birth_date = datetime.strptime(birth_date_gregorian, '%Y-%m-%d').date()
                today = now().date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if birth_date >= today or age < 18:
                    messages.error(request, 'تاریخ تولد نامعتبر است. باید حداقل 18 سال سن داشته باشید.')
                    is_valid = False
            except ValueError as e:
                messages.error(request, f'فرمت تاریخ تولد نامعتبر است: {str(e)}')
                is_valid = False
        else:
            messages.error(request, 'تاریخ تولد اجباری است.')
            is_valid = False

        # کپی شناسنامه
        if id_copy:
            max_size = 5 * 1024 * 1024  # 5MB
            if not id_copy.content_type.startswith(('image/', 'application/pdf')) or id_copy.size > max_size:
                messages.error(request, 'فایل کپی شناسنامه باید تصویر یا PDF باشد و حداکثر 5 مگابایت.')
                is_valid = False

        # آدرس
        if not address:
            messages.error(request, 'آدرس اجباری است.')
            is_valid = False

        # اگر همه اعتبارسنجی‌ها درست بود، مشتری رو ذخیره کن
        if is_valid:
            try:
                customer = Customer.objects.create(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    national_id=national_id,
                    id_number=id_number,
                    phone_number=phone_number,
                    email=email if email else None,
                    birth_date=birth_date,
                    gender=gender if gender else None,
                    customer_type=customer_type if customer_type else None,
                    address=address,
                    id_copy=id_copy
                )
                # ایجاد موجودی اولیه برای مشتری
                Balance.objects.create(customer=customer, amount=0)
                messages.success(request, 'مشتری با موفقیت ایجاد شد.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'خطا در ایجاد مشتری: {str(e)}')

    return render(request, 'core/create_customer.html')


@login_required
def customer_detail_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    loans = Loan.objects.filter(customer=customer)
    accounts = Account.objects.filter(customer=customer)
    transactions = Transaction.objects.filter(account__customer=customer)

    # تبدیل تاریخ‌ها به شمسی
    for transaction in transactions:
        transaction.date_shamsi = jdatetime.datetime.fromgregorian(datetime=transaction.date).strftime('%Y/%m/%d %H:%M')

    context = {
        'customer': customer,
        'loans': loans,
        'accounts': accounts,
        'transactions': transactions,
    }
    return render(request, 'core/customer_detail.html', context)


@login_required
def customer_search_view(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(
            first_name__icontains=query
        ) | customers.filter(
            last_name__icontains=query
        ) | customers.filter(
            national_code__icontains=query
        )

    context = {
        'customers': customers,
        'query': query,
    }
    return render(request, 'core/customer_search.html', context)


@login_required
def create_account_view(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        balance = request.POST['balance']
        customer_id = request.POST['customer_id']

        try:
            customer = Customer.objects.get(id=customer_id)
            Account.objects.create(
                customer=customer,
                account_number=account_number,
                balance=balance
            )
            messages.success(request, 'حساب با موفقیت ایجاد شد.')
            return redirect('dashboard')
        except Customer.DoesNotExist:
            messages.error(request, 'مشتری یافت نشد.')
        except Exception as e:
            messages.error(request, f'خطا در ایجاد حساب: {str(e)}')

    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'core/create_account.html', context)