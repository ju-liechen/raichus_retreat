from django.urls import path

from . import views


app_name = 'bank'
urlpatterns = [
    path('bank/', views.BankDashboardView.as_view(), name='bank_dashboard'),
    path('clear-link-token/', views.clear_link_token, name='clear-link-token'),
    path('plaid/', views.plaid_connect, name='plaid-connect')
]
