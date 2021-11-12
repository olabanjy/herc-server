from django.contrib import admin
from .models import Loan, AppliedLoan

# Register your models here.

admin.site.register(Loan)
admin.site.register(AppliedLoan)
