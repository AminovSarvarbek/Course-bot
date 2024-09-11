from django.urls import path
from .views import unpaidPaymentsView, revenue_view

app_name = 'payment'
urlpatterns = [
    path('unpaid/', unpaidPaymentsView, name='unpaid'),
    path('revenue/', revenue_view, name='revenue'),
]