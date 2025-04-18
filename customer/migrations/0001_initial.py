# Generated by Django 5.1 on 2025-04-01 17:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('national_id', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'کد ملی باید ۱۰ رقمی باشد')], verbose_name='کد ملی')),
                ('id_number', models.CharField(max_length=20, verbose_name='شماره شناسنامه')),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='شماره تلفن باید با 09 شروع شود و 11 رقم باشد (مثال: 09123456789)', regex='^09\\d{9}$')], verbose_name='شماره تلفن')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='ایمیل')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.CharField(blank=True, choices=[('male', 'مرد'), ('female', 'زن')], max_length=10, null=True, verbose_name='جنسیت')),
                ('customer_type', models.CharField(blank=True, choices=[('regular', 'عادی'), ('vip', 'ویژه')], max_length=10, null=True, verbose_name='نوع مشتری')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('id_copy', models.FileField(blank=True, null=True, upload_to='id_copies/', verbose_name='کپی شناسنامه')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'مشتریان',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')),
                ('is_read', models.BooleanField(default=False, verbose_name='خوانده شده')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='customer.customer', verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام\u200cها',
            },
        ),
    ]
