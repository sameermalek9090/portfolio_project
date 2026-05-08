from django.urls import path
from .views import login_view, verify_otp

urlpatterns = [
    path('login/', login_view, name='login'),
    path('verify/', verify_otp, name='verify_otp'),
]