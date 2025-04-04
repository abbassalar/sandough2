from django.db import models
from customer.models import Customer

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="مبلغ وام")
    date_issued = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ صدور")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="نرخ سود")
    duration_months = models.IntegerField(verbose_name="مدت زمان (ماه)")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده")

    def __str__(self):
        return f"Loan for {self.customer} - {self.amount}"

    class Meta:
        verbose_name = "وام"
        verbose_name_plural = "وام‌ها"

class InstallmentPlan(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='installment_plans')
    number_of_installments = models.IntegerField(verbose_name="تعداد اقساط")
    amount_per_installment = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="مبلغ هر قسط")
    start_date = models.DateField(verbose_name="تاریخ شروع")

    def __str__(self):
        return f"Plan for {self.loan} - {self.number_of_installments} installments"

    class Meta:
        verbose_name = "طرح قسط"
        verbose_name_plural = "طرح‌های قسط"

class InstallmentPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='installment_payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="مبلغ پرداخت")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ پرداخت")

    def __str__(self):
        return f"Payment for {self.loan} - {self.amount}"

    class Meta:
        verbose_name = "پرداخت قسط"
        verbose_name_plural = "پرداخت‌های قسط"