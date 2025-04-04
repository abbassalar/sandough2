from django.db import models
from customer.models import Customer

class Balance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='balances')
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="موجودی کل")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="آخرین به‌روزرسانی")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # برای ذخیره موجودی

    def __str__(self):
        return f"{self.customer} - {self.total_balance}"

    class Meta:
        verbose_name = "موجودی"
        verbose_name_plural = "موجودی‌ها"