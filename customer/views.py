from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm

@login_required
def create_customer_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # ارتباط مشتری با کاربر لاگین‌شده
            customer.save()
            return redirect('customer_search')
    else:
        form = CustomerForm()
    return render(request, 'customer/create_customer.html', {'form': form})

@login_required
def customer_search_view(request):
    query = request.GET.get('query', '')
    customers = []
    if query:
        customers = Customer.objects.filter(
            models.Q(national_id=query) |
            models.Q(account_number=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )
    return render(request, 'customer/customer_search.html', {'customers': customers, 'query': query})

@login_required
def customer_detail_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'customer/customer_detail.html', {'customer': customer})