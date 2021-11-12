from rest_framework import serializers
from .models import *
from authentication.models import User
from authentication.serializers import UserSerializer




class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id','name','price']
    
  

class AppliedLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedLoan
        exclude = ("id",)
    

