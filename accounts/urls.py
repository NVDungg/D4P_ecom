from django.urls import path
from .views import register, login, logout, activate, dashbroad, forgot_password, resetpassword, resetpassword_validate, my_orders, edit_profile, change_password, order_detail

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

    #For User change
    path('my_orders/', my_orders, name='my_orders'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('order_detail/', order_detail, name='order_detail'),

]
