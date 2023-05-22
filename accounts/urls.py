from django.urls import path
from .views import register, login, logout, activate

urlpatterns = [
    path('', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    #acctive link get uid n token form register
    path("activate/<uidb64>/<token>/", activate, name="activate")
]
