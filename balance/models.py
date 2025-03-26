from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_balance}"