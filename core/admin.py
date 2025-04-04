from django.contrib import admin
from .models import Account, Transaction, UserProfile  # حذف Customer
from customer.models import Customer  # وارد کردن Customer از اپ customer

# ثبت مدل‌ها
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transaction)  # اصلاح شده به Transaction

# ثبت مدل UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'national_code', 'address')
    search_fields = ('user__username', 'national_code')
    list_filter = ('user',)