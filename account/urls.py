from django.urls import path
from account import views

app_name = "account"

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('test-email/', views.test_email, name='test-email'),
    path('test-template/', views.test_activation_template, name='test-template'),
    path('test-email-config/', views.test_email_config, name='test-email-config'),
]
