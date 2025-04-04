from django import forms
from django.core.validators import RegexValidator  # وارد کردن RegexValidator
from .models import Customer
from core.models import Account

class CustomerForm(forms.ModelForm):
    account_number = forms.CharField(
        max_length=20,
        label="شماره حساب",
        validators=[RegexValidator(r'^\d+$', 'شماره حساب باید فقط شامل اعداد باشد')]  # اصلاح forms.RegexValidator به RegexValidator
    )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'national_id', 'id_number', 'phone_number', 'address', 'id_copy']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'national_id': 'کد ملی',
            'id_number': 'شماره شناسنامه',
            'phone_number': 'شماره تلفن',
            'address': 'آدرس',
            'id_copy': 'کپی شناسنامه',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if Customer.objects.exclude(pk=self.instance.pk).filter(national_id=national_id).exists():
            raise forms.ValidationError('این کد ملی قبلاً ثبت شده است.')
        return national_id

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Customer.objects.exclude(pk=self.instance.pk).filter(phone_number=phone_number).exists():
            raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است.')
        return phone_number

    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']
        if Account.objects.filter(account_number=account_number).exists():
            raise forms.ValidationError('این شماره حساب قبلاً ثبت شده است.')
        return account_number