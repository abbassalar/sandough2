from django.db import models
from core.models import Account

class Withdrawal(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="مبلغ برداشت")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ برداشت")

    def __str__(self):
        return f"Withdrawal from {self.account} - {self.amount}"

    class Meta:
        verbose_name = "برداشت"
        verbose_name_plural = "برداشت‌ها"