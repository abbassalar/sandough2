from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from loan.models import Loan

class InstallmentPlan(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_installments = models.IntegerField()
    amount_per_installment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()

    def __str__(self):
        return f"Plan for {self.loan} - {self.number_of_installments} installments"