from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['national_id', 'account_number', 'id_number', 'first_name', 'last_name', 'phone_number', 'address', 'id_copy']
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
        if len(national_id) != 10 or not national_id.isdigit():
            raise forms.ValidationError("کد ملی باید 10 رقم باشد و فقط شامل اعداد باشد.")
        return national_id