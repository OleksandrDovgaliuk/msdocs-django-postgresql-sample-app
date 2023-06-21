from django.urls import path, reverse_lazy
from .views import signup, signup_done, signup_confirm, log_in, settings

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signup/done/', signup_done, name='signup_done'),
    path('signup/confirm/<str:activation_key>/', signup_confirm, name='signup_confirm'),
    path('login/', log_in, name='login'),
    path('settings', settings, name='settings')
]
