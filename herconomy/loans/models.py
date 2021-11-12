from django.db import models
from django.conf import settings
from authentication.models import User

# Create your models here.


class Loan(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class AppliedLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} ---{self.loan.price}"


