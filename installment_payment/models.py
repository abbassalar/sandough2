from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from loan.models import Loan

class InstallmentPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.loan} - {self.amount}"