from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('payroll/', views.payroll_view, name='payroll_view'),
    path('payslip/<int:payslip_id>/', views.payslip_view, name='payslip_view'),
    path('payslip/<int:payslip_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('login/', views.login_view, name='login_view'),
     path('login-action/', views.login_action, name='login_action'),

]