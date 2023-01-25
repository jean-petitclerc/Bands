from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_account, name='register_account'),
    path('logout/', views.logout_account, name='logout_account'),
    path('login/', views.login_account, name='login_account'),
]
