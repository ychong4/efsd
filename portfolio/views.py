from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.core.mail import EmailMultiAlternatives
from io import BytesIO

now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'home': home})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    page = request.GET.get('page', 1)

    paginator = Paginator(customer, 5)
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    return render(request, 'portfolio/customer_list.html',
                 {'customers': customers})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'portfolio/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
   stocks = Stock.objects.all()
   page = request.GET.get('page', 1)

   paginator = Paginator(stocks, 5)
   try:
       stock = paginator.page(page)
   except PageNotAnInteger:
       stock = paginator.page(1)
   except EmptyPage:
       stock = paginator.page(paginator.num_pages)
   return render(request, 'portfolio/stock_list.html', {'stocks': stock})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.purchased_date = timezone.now()
           stock.save()
           stocks = Stock.objects.all()
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    return redirect('portfolio:stock_list')

@login_required
def investment_list(request):
   investments = Investment.objects.all()
   page = request.GET.get('page', 1)

   paginator = Paginator(investments, 5)
   try:
       investment = paginator.page(page)
   except PageNotAnInteger:
       investment = paginator.page(1)
   except EmptyPage:
       investment = paginator.page(paginator.num_pages)
   return render(request, 'portfolio/investment_list.html', {'investments': investment})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.all()
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # stock.customer = stock.id
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    return redirect('portfolio:investment_list')

@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   mutualFunds = MutualFund.objects.filter(customer=pk)
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))['recent_value__sum' or 0.00]
   if sum_recent_value == None:
       sum_recent_value = 0
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))['acquired_value__sum' or 0.00]
   if sum_acquired_value == None:
       sum_acquired_value = 0
   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0
   mutualFund_recent_value = MutualFund.objects.filter(customer=pk).aggregate(Sum('recent_value'))['recent_value__sum' or 0.00]
   if mutualFund_recent_value == None:
       mutualFund_recent_value = 0
   mutualFund_acquired_value = MutualFund.objects.filter(customer=pk).aggregate(Sum('acquired_value'))[
       'acquired_value__sum' or 0.00]
   if mutualFund_acquired_value == None:
       mutualFund_acquired_value = 0

   # Loop through each stock and add the value to the total
   for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

   result_of_total_stocks = float(sum_current_stocks_value) - float(sum_of_initial_stock_value)

   result_of_total_investment = float(sum_recent_value) - float(sum_acquired_value)

   result_of_total_mutualFund = float(mutualFund_recent_value) - float(mutualFund_acquired_value)

   portfolio_initial_investment = float(sum_acquired_value) + float(sum_of_initial_stock_value) + float(mutualFund_acquired_value)
   portfolio_current_investment = float(sum_recent_value) + float(sum_current_stocks_value) + float(mutualFund_recent_value)
   grand_total_result = float(portfolio_initial_investment) + float(portfolio_current_investment)

   return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                       'customer': customer,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'mutualFunds': mutualFunds,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                       'sum_current_stocks_value': sum_current_stocks_value,
                                                       'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                       'result_of_total_stocks': result_of_total_stocks,
                                                       'result_of_total_investment': result_of_total_investment,
                                                       'portfolio_initial_investment': portfolio_initial_investment,
                                                       'portfolio_current_investment': portfolio_current_investment,
                                                       'mutualFund_acquired_value': mutualFund_acquired_value,
                                                       'mutualFund_recent_value': mutualFund_recent_value,
                                                       'result_of_total_mutualFund': result_of_total_mutualFund,
                                                       'grand_total_result': grand_total_result})

@login_required
def mutual_fund_list(request):
   mutualFunds = MutualFund.objects.all()
   page = request.GET.get('page', 1)

   paginator = Paginator(mutualFunds, 5)
   try:
       mutualFund = paginator.page(page)
   except PageNotAnInteger:
       mutualFund = paginator.page(1)
   except EmptyPage:
       mutualFund = paginator.page(paginator.num_pages)
   return render(request, 'portfolio/mutual_fund_list.html', {'mutualFunds': mutualFund})

@login_required
def mutual_fund_new(request):
   if request.method == "POST":
       form = MutualFundForm(request.POST)
       if form.is_valid():
           mutualFund = form.save(commit=False)
           mutualFund.created_date = timezone.now()
           mutualFund.save()
           mutualFunds = MutualFund.objects.all()
           return render(request, 'portfolio/mutual_fund_list.html',
                         {'mutualFunds': mutualFunds})
   else:
       form = MutualFundForm()
       # print("Else")
   return render(request, 'portfolio/mutual_fund_new.html', {'form': form})

@login_required
def mutual_fund_edit(request, pk):
   mutualFund = get_object_or_404(MutualFund, pk=pk)
   if request.method == "POST":
       form = MutualFundForm(request.POST, instance=mutualFund)
       if form.is_valid():
           mutualFund = form.save()
           # stock.customer = stock.id
           mutualFund.updated_date = timezone.now()
           mutualFund.save()
           mutualFunds = MutualFund.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/mutual_fund_list.html', {'mutualFunds': mutualFunds})
   else:
       # print("else")
       form = MutualFundForm(instance=mutualFund)
   return render(request, 'portfolio/mutual_fund_edit.html', {'form': form})

@login_required
def mutual_fund_delete(request, pk):
    mutualFund = get_object_or_404(MutualFund, pk=pk)
    mutualFund.delete()
    return redirect('portfolio:mutual_fund_list')

def portfolio_pdf(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutualFunds = MutualFund.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))[
        'recent_value__sum' or 0.00]
    if sum_recent_value == None:
        sum_recent_value = 0
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))[
        'acquired_value__sum' or 0.00]
    if sum_acquired_value == None:
        sum_acquired_value = 0
    # overall_investment_results = sum_recent_value-sum_acquired_value
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    mutualFund_recent_value = MutualFund.objects.filter(customer=pk).aggregate(Sum('recent_value'))[
        'recent_value__sum' or 0.00]
    if mutualFund_recent_value == None:
        mutualFund_recent_value = 0
    mutualFund_acquired_value = MutualFund.objects.filter(customer=pk).aggregate(Sum('acquired_value'))[
        'acquired_value__sum' or 0.00]
    if mutualFund_acquired_value == None:
        mutualFund_acquired_value = 0

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

    result_of_total_stocks = float(sum_current_stocks_value) - float(sum_of_initial_stock_value)

    result_of_total_investment = float(sum_recent_value) - float(sum_acquired_value)

    result_of_total_mutualFund = float(mutualFund_recent_value) - float(mutualFund_acquired_value)

    portfolio_initial_investment = float(sum_acquired_value) + float(sum_of_initial_stock_value) + float(
        mutualFund_acquired_value)
    portfolio_current_investment = float(sum_recent_value) + float(sum_current_stocks_value) + float(
        mutualFund_recent_value)
    grand_total_result = float(portfolio_initial_investment) + float(portfolio_current_investment)

    html = render_to_string('portfolio/pdf.html',
                            {'customers': customers,
                             'customer': customer,
                             'investments': investments,
                             'stocks': stocks,
                             'mutualFunds': mutualFunds,
                             'sum_acquired_value': sum_acquired_value,
                             'sum_recent_value': sum_recent_value,
                             'sum_current_stocks_value': sum_current_stocks_value,
                             'sum_of_initial_stock_value': sum_of_initial_stock_value,
                             'result_of_total_stocks': result_of_total_stocks,
                             'result_of_total_investment': result_of_total_investment,
                             'portfolio_initial_investment': portfolio_initial_investment,
                             'portfolio_current_investment': portfolio_current_investment,
                             'mutualFund_acquired_value': mutualFund_acquired_value,
                             'mutualFund_recent_value': mutualFund_recent_value,
                             'result_of_total_mutualFund': result_of_total_mutualFund,
                             'grand_total_result': grand_total_result})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{pk}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + '/admin/css/base.css')])
    return response

def email(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    mutualFunds = MutualFund.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))[
        'recent_value__sum' or 0.00]
    if sum_recent_value == None:
        sum_recent_value = 0
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))[
        'acquired_value__sum' or 0.00]
    if sum_acquired_value == None:
        sum_acquired_value = 0
    # overall_investment_results = sum_recent_value-sum_acquired_value
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    mutualFund_recent_value = MutualFund.objects.filter(customer=pk).aggregate(Sum('recent_value'))[
        'recent_value__sum' or 0.00]
    if mutualFund_recent_value == None:
        mutualFund_recent_value = 0
    mutualFund_acquired_value = MutualFund.objects.filter(customer=pk).aggregate(Sum('acquired_value'))[
        'acquired_value__sum' or 0.00]
    if mutualFund_acquired_value == None:
        mutualFund_acquired_value = 0

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

    result_of_total_stocks = float(sum_current_stocks_value) - float(sum_of_initial_stock_value)

    result_of_total_investment = float(sum_recent_value) - float(sum_acquired_value)

    result_of_total_mutualFund = float(mutualFund_recent_value) - float(mutualFund_acquired_value)

    portfolio_initial_investment = float(sum_acquired_value) + float(sum_of_initial_stock_value) + float(
        mutualFund_acquired_value)
    portfolio_current_investment = float(sum_recent_value) + float(sum_current_stocks_value) + float(
        mutualFund_recent_value)
    grand_total_result = float(portfolio_initial_investment) + float(portfolio_current_investment)
    if request.method == "POST":
        form = EmailForm(request.POST, instance=customer)
        if form.is_valid():
            subject = 'Your Portfolio Information'
            from_email = 'ychongdjangotest@gmail.com'
            to_email = form.cleaned_data['email']
            message = 'Please, find attached the portfolio information.'
            email = EmailMultiAlternatives(subject, message, from_email, [to_email])
            # generate PDF
            html = render_to_string('portfolio/pdf.html',
                                    {'customers': customers,
                                     'customer': customer,
                                     'investments': investments,
                                     'stocks': stocks,
                                     'mutualFunds': mutualFunds,
                                     'sum_acquired_value': sum_acquired_value,
                                     'sum_recent_value': sum_recent_value,
                                     'sum_current_stocks_value': sum_current_stocks_value,
                                     'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                     'result_of_total_stocks': result_of_total_stocks,
                                     'result_of_total_investment': result_of_total_investment,
                                     'portfolio_initial_investment': portfolio_initial_investment,
                                     'portfolio_current_investment': portfolio_current_investment,
                                     'mutualFund_acquired_value': mutualFund_acquired_value,
                                     'mutualFund_recent_value': mutualFund_recent_value,
                                     'result_of_total_mutualFund': result_of_total_mutualFund,
                                     'grand_total_result': grand_total_result})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/admin/css/base.css')]
            weasyprint.HTML(string=html).write_pdf(out,
                                                   stylesheets=stylesheets)
            email.attach(f'customer_{customer.name}.pdf', out.getvalue(), 'application/pdf')
            email.send()
            return redirect('portfolio:successView')

    else:
        form = EmailForm(instance=customer)
    return render(request, 'portfolio/portfolio_email.html', {'form': form})

def successView(request):
    return render(request, 'portfolio/successView.html',
                  {'successView': successView})

# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):
    def get(self, request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)
