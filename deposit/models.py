from django.db import models
from core.models import Account

class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="مبلغ واریز")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ واریز")

    def __str__(self):
        return f"Deposit to {self.account} - {self.amount}"

    class Meta:
        verbose_name = "واریز"
        verbose_name_plural = "واریزها"