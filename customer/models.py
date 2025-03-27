from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    national_id = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    account_number = models.CharField(max_length=20, unique=True, verbose_name="شماره حساب")
    id_number = models.CharField(max_length=20, verbose_name="شماره شناسنامه")
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس")
    id_copy = models.FileField(upload_to='id_copies/', null=True, blank=True, verbose_name="کپی شناسنامه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری‌ها"

class Message(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='messages', verbose_name="مشتری")
    content = models.TextField(verbose_name="محتوای پیام")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    is_read = models.BooleanField(default=False, verbose_name="خوانده‌شده")

    def __str__(self):
        return f"پیام به {self.customer.first_name} {self.customer.last_name} - {self.sent_at}"

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"