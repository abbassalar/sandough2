# Generated by Django 5.1 on 2025-04-01 17:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20, unique=True, verbose_name='شماره حساب')),
                ('account_type', models.CharField(choices=[('SAVINGS', 'پس\u200cانداز'), ('CHECKING', 'جاری')], default='SAVINGS', max_length=50, verbose_name='نوع حساب')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='موجودی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='customer.customer')),
            ],
            options={
                'verbose_name': 'حساب',
                'verbose_name_plural': 'حساب\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='customer.customer')),
            ],
            options={
                'verbose_name': 'اعلان',
                'verbose_name_plural': 'اعلان\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'واریز'), ('WITHDRAWAL', 'برداشت'), ('TRANSFER', 'انتقال')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='core.account')),
            ],
            options={
                'verbose_name': 'تراکنش',
                'verbose_name_plural': 'تراکنش\u200cها',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('national_code', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'پروفایل کاربر',
                'verbose_name_plural': 'پروفایل\u200cهای کاربران',
            },
        ),
    ]
