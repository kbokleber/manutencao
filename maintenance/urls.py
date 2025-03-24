from django.urls import path
from .views import (
    CreateOrderView, CreateEquipmentView, DetailOrderView,
    DeleteOrderView, UpdateOrderView, MaintenanceOrderListView
)

app_name = 'maintenance'

urlpatterns = [
    path('order/create/', CreateOrderView.as_view(), name='order_create'),
    path('order/<int:pk>/', DetailOrderView.as_view(), name='order_detail'),
    path('order/<int:pk>/edit/', UpdateOrderView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', DeleteOrderView.as_view(), name='order_delete'),
    path('equipment/create/', CreateEquipmentView.as_view(), name='equipment_create'),
    path('orders/', MaintenanceOrderListView.as_view(), name='order_list'),
    # As URLs serão adicionadas posteriormente
] 