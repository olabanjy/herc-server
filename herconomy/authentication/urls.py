from django.urls import path

from .views import RegistrationAPIView, ModeratorRegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, ProfileDetailView

app_name = 'authentication'
urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
    path('users/mod/', ModeratorRegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),

    path('user/profile/<user_email>/', ProfileDetailView.as_view()),
]