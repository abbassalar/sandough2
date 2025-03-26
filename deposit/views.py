from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Deposit

@login_required
def deposit_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        Deposit.objects.create(user=request.user, amount=amount)
        return render(request, 'deposit/success.html')
    return render(request, 'deposit/deposit.html')