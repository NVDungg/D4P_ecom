from django.urls import path
from .views import register, login, logout, activate, dashbroad

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path("dashbroad/", dashbroad, name="dashbroad"),
    path("", dashbroad, name="dashbroad"),

    #acctive link get uid n token form register
    path("activate/<uidb64>/<token>/", activate, name="activate")
]
