from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import UserProfile

# فرم ثبت‌نام (بدون تغییر)
class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        label="نام",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=50,
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="نام کاربری فقط می‌تواند شامل حروف، اعداد و کاراکترهای @/./+/-/_ باشد."
            )
        ]
    )
    email = forms.EmailField(
        required=False,  # غیرضروری کردن ایمیل
        label="ایمیل (اختیاری)",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=11,
        label="شماره تلفن",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="شماره تلفن باید با 09 شروع شود و 11 رقم باشد (مثال: 09123456789)"
            )
        ]
    )
    national_code = forms.CharField(
        max_length=11,
        label="کد ملی",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="کد ملی باید دقیقاً 10 رقم باشد."
            )
        ]
    )
    address = forms.CharField(
        label="آدرس",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$',
                message="رمز عبور باید حداقل 6 کاراکتر باشد و شامل حداقل یک حرف و یک عدد باشد."
            )
        ]
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        # می‌تونی اعتبارسنجی پیشرفته‌تر برای کد ملی اضافه کنی
        return national_code

# فرم ویرایش پروفایل
class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=11,
        label="شماره تلفن",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="شماره تلفن باید با 09 شروع شود و 11 رقم باشد (مثال: 09123456789)"
            )
        ]
    )
    national_code = forms.CharField(
        max_length=11,
        label="کد ملی",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="کد ملی باید دقیقاً 10 رقم باشد."
            )
        ]
    )

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'national_code', 'address']
        labels = {
            'phone_number': 'شماره تلفن',
            'national_code': 'کد ملی',
            'address': 'آدرس',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        # می‌تونی اعتبارسنجی پیشرفته‌تر برای کد ملی اضافه کنی
        return national_code