from django.urls import path

from . import views


app_name = 'bank'
urlpatterns = [
    path('bank/', views.BankDashboardView.as_view(), name='bank_dashboard'),
]
