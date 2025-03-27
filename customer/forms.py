from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['national_id', 'account_number', 'id_number', 'first_name', 'last_name', 'phone_number', 'address',
                  'id_copy']
        labels = {
            'national_id': 'کد ملی',
            'account_number': 'شماره حساب',
            'id_number': 'شماره شناسنامه',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تماس',
            'address': 'آدرس',
            'id_copy': 'کپی شناسنامه',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']

        # چک کردن طول و اینکه فقط عدد باشه
        if len(national_id) != 10 or not national_id.isdigit():
            raise forms.ValidationError("کد ملی باید 10 رقم باشد و فقط شامل اعداد باشد.")

        # چک کردن اینکه همه ارقام یکسان نباشن (مثلاً 1111111111)
        if len(set(national_id)) == 1:
            raise forms.ValidationError("کد ملی معتبر نیست (همه ارقام یکسان هستند).")

        # الگوریتم اعتبارسنجی کد ملی
        check_digit = int(national_id[-1])  # رقم آخر (رقم کنترلی)
        total = 0
        for i in range(9):
            total += int(national_id[i]) * (10 - i)
        remainder = total % 11
        if remainder < 2:
            expected_check_digit = remainder
        else:
            expected_check_digit = 11 - remainder

        if check_digit != expected_check_digit:
            raise forms.ValidationError("کد ملی معتبر نیست.")

        return national_id