from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    national_code = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"

class Account(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True, verbose_name="شماره حساب")
    account_type = models.CharField(max_length=50, choices=[
        ('SAVINGS', 'پس‌انداز'),
        ('CHECKING', 'جاری'),
    ], default='SAVINGS', verbose_name="نوع حساب")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name="موجودی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.customer} - {self.account_number} - {self.account_type} - {self.balance}"

    class Meta:
        verbose_name = "حساب"
        verbose_name_plural = "حساب‌ها"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50, choices=[
        ('DEPOSIT', 'واریز'),
        ('WITHDRAWAL', 'برداشت'),
        ('TRANSFER', 'انتقال'),
    ])
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.date}"

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

class Notification(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.customer} - {self.created_at}"

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان‌ها"