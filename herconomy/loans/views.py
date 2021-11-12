from rest_framework import serializers, status
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import AppliedLoan, Loan
from authentication.models import User
from .serializers import LoanSerializer, AppliedLoanSerializer


class LoansListView(generics.ListAPIView):
    queryset = Loan.objects.all().order_by("-id")
    permission_classes = (AllowAny,)
    serializer_class = LoanSerializer





class AppliedLoanListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        applied_loans = AppliedLoan.objects.all()
        serializer = AppliedLoanSerializer(applied_loans, many=True)
        return_data = []
        for app_loan in applied_loans:
            return_data.append({
                '_id':app_loan.id,
                'loan_name':app_loan.loan.name,
                'loan_price':app_loan.loan.price,
                'approved':app_loan.approved
            })
        return Response(data=return_data)

    def post(self, request):
        print(request.data)
        user_email = request.data['user']
        the_user = get_object_or_404(User, email=user_email)
        valid_data ={
            'user':the_user.id,
            'loan':request.data['loan']
        }
        print(valid_data)
        serializer = AppliedLoanSerializer(data=valid_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

        
class ApplliedLoanDetailView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, the_pk):
        the_applied_loan = get_object_or_404(AppliedLoan, pk=the_pk)
        return the_applied_loan
    
    def get(self, request, the_pk, format=None):
        the_applied_loan = self.get_object(the_pk)
        serializer = AppliedLoanSerializer(the_applied_loan)
        return Response(serializer.data)

    
    def patch(self, request, the_pk):
        print(request.data)
        the_loan = self.get_object(the_pk)
        serializer = AppliedLoanSerializer(the_loan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserApplied(APIView):
    permission_classes = (AllowAny,)

    def get(self, request,user_email, format=None):
        the_user = get_object_or_404(User, email=user_email)
        user_applied_loans = AppliedLoan.objects.filter(user=the_user).all()
        serializer = AppliedLoanSerializer(user_applied_loans, many=True)
        return_data = []
       
        for app_loan in user_applied_loans:
            return_data.append({
                '_id':app_loan.id,
                'loan_name':app_loan.loan.name,
                'loan_price':app_loan.loan.price,
                'approved':app_loan.approved
            })
  
        print(return_data)

        return Response(data=return_data)


    
