# core/models.py
from django.db import models
from django.core.validators import RegexValidator

class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_id = models.CharField(
        max_length=10, unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید ۱۰ رقمی باشد')],
        verbose_name="کد ملی"
    )
    phone_number = models.CharField(max_length=11, verbose_name="شماره تلفن")
    address = models.TextField(verbose_name="آدرس")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True, verbose_name="شماره حساب")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="مشتری")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="موجودی")

    def __str__(self):
        return self.account_number

    class Meta:
        verbose_name = "حساب"
        verbose_name_plural = "حساب‌ها"

class Transaction(models.Model):
    TRANSACTION_TYPES = (('deposit', 'دریافت'), ('withdraw', 'پرداخت'))
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="حساب")
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="نوع تراکنش")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="مبلغ")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ")

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}"

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"