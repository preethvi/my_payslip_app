from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import EmployeePayslip
from datetime import date
import calendar
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login_view(request):
    return render(request, 'login.html')

def login_action(request):
    if request.method == 'POST':
        # Retrieve the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user if authentication is successful
            login(request, user)
            # Redirect to the payroll page after login
            return redirect('payroll_view')
        else:
            # Return error if authentication fails
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error': error_message})

    # If the request is not POST, redirect to the login page
    return redirect('login_view')

# Home Page View
def home_view(request):
    # Here you can pass data for the calendar, meetings, etc.
    # For now, we'll just render the template.
    return render(request, 'home.html')

# Payroll Form View
def payroll_view(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        employee_id = request.POST.get('employee_id')
        month_str = request.POST.get('month')
        
        # Convert month string to date object
        month_date = date.fromisoformat(f"{month_str}-01")
        
        present_days = int(request.POST.get('present_days'))
        additions = float(request.POST.get('additions', 0))
        
        # Get total days in the selected month
        total_days_in_month = calendar.monthrange(month_date.year, month_date.month)[1]
        
        # Calculate other values
        per_day_salary = 300.00
        working_days = total_days_in_month
        leave_days = working_days - present_days
        deductions = leave_days * per_day_salary
        total_salary = present_days * per_day_salary
        # grand_total = total_salary - deductions + additions
        grand_total = total_salary + additions

        # Save to database
        payslip = EmployeePayslip.objects.create(
            name=name,
            roll=roll,
            employee_id=employee_id,
            month=month_date,
            working_days=working_days,
            leave_days=leave_days,
            present_days=present_days,
            deductions=deductions,
            additions=additions,
            total_salary=total_salary,
            grand_total=grand_total
        )
        
        # Redirect to payslip page with the new payslip ID
        return redirect('payslip_view', payslip_id=payslip.id)
    
    # Context for the form page
    context = {
        'today': date.today(),
    }
    
    return render(request, 'payroll.html', context)

# Payslip Detail View
def payslip_view(request, payslip_id):
    payslip = get_object_or_404(EmployeePayslip, id=payslip_id)
    return render(request, 'payslip.html', {'payslip': payslip})

# PDF Generation View
def generate_pdf(request, payslip_id):
    payslip = get_object_or_404(EmployeePayslip, id=payslip_id)
    template = get_template('payslip_pdf.html')
    html = template.render({'payslip': payslip})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{payslip.name.replace(" ", "_")}_payslip.pdf"'
    
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
