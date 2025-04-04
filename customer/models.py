from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Customer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customers',
        verbose_name="کاربر"
    )
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید ۱۰ رقمی باشد')],
        verbose_name="کد ملی"
    )
    id_number = models.CharField(max_length=20, verbose_name="شماره شناسنامه")
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="شماره تلفن باید با 09 شروع شود و 11 رقم باشد (مثال: 09123456789)"
            )
        ],
        verbose_name="شماره تلفن"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="ایمیل"
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تولد"
    )
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'مرد'), ('female', 'زن')],
        null=True,
        blank=True,
        verbose_name="جنسیت"
    )
    customer_type = models.CharField(
        max_length=10,
        choices=[('regular', 'عادی'), ('vip', 'ویژه')],
        null=True,
        blank=True,
        verbose_name="نوع مشتری"
    )
    address = models.TextField(verbose_name="آدرس")
    id_copy = models.FileField(
        upload_to='id_copies/',
        null=True,
        blank=True,
        verbose_name="کپی شناسنامه"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

class Message(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="مشتری"
    )
    content = models.TextField(verbose_name="محتوا")
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="خوانده شده"
    )

    def __str__(self):
        return f"Message to {self.customer} at {self.sent_at}"

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"