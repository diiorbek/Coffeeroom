from django.urls import path
from .views import ActiveOrdersView, HistoryOrdersView

urlpatterns = [
    path('orders/active/<int:user_id>/', ActiveOrdersView.as_view(), name='active-orders'),
    path('orders/history/<int:user_id>/', HistoryOrdersView.as_view(), name="history-orders")
]