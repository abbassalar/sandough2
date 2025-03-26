from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Withdrawal

@login_required
def withdrawal_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        Withdrawal.objects.create(user=request.user, amount=amount)
        return render(request, 'withdrawal/success.html')
    return render(request, 'withdrawal/withdrawal.html')