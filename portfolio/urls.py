from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_change_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/create/', views.investment_new, name='investment_new'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    path('customers_json/', views.CustomerList.as_view(), name='customer_json'),
    path('mutual_fund_list', views.mutual_fund_list, name='mutual_fund_list'),
    path('mutual_fund/create/', views.mutual_fund_new, name='mutual_fund_new'),
    path('mutual_fund/<int:pk>/edit/', views.mutual_fund_edit, name='mutual_fund_edit'),
    path('mutual_fund/<int:pk>/delete/', views.mutual_fund_delete, name='mutual_fund_delete'),
    path('customer/<int:pk>/pdf/', views.portfolio_pdf, name='portfolio_pdf'),
    path('customer/<int:pk>/email/', views.email, name='portfolio_email'),
    path('customer/email/success/', views.successView, name='successView'),
]

urlpatterns = format_suffix_patterns(urlpatterns)