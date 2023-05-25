from django.urls import path
from .views import register, login, logout, activate, dashbroad, forgot_password, resetpassword, resetpassword_validate

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path("dashbroad/", dashbroad, name="dashbroad"),
    path("", dashbroad, name="dashbroad"),

    #acctive link get uid n token form register
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("getpassword/", forgot_password, name="forgot_password"),
    path("resetpassword_validate/<uidb64>/<token>/", resetpassword_validate, name="resetpassword_validate"),
    path("resetpassword/", resetpassword, name="resetpassword"),

]
