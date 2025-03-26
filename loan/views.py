from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Loan

@login_required
def loan_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        Loan.objects.create(user=request.user, amount=amount)
        return render(request, 'loan/success.html')
    return render(request, 'loan/loan.html')