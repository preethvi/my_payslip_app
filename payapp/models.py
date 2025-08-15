from django.db import models

class EmployeePayslip(models.Model):
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20)
    month = models.DateField()
    
    working_days = models.IntegerField()
    leave_days = models.IntegerField(default=0)
    present_days = models.IntegerField()
    
    per_day_salary = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    additions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name}'s Payslip for {self.month.strftime('%B %Y')}"
