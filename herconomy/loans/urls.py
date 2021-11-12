from django.urls import path
from .views import *

app_name = 'loans'

urlpatterns = [
    path('', LoansListView.as_view()),
    path('applied-loans/', AppliedLoanListView.as_view()),
    path('applied-loan/<the_pk>/', ApplliedLoanDetailView.as_view()),
    path('user-applied-loans/<user_email>/', GetUserApplied.as_view()),


  
]