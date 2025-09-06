from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouse_base, name='warehouse_base'),
    path('dashboard/', views.warehouse_dashboard, name='warehouse_dashboard'),
    path('inventory/', views.warehouse_inventory, name='warehouse_inventory'),
    path('forecast/', views.warehouse_forecast, name='warehouse_forecast'),
    path('spare_parts_listing/', views.warehouse_spare_parts_listing, name='warehouse_spare_parts_listing'),
    path('orders/', views.warehouse_orders, name='warehouse_orders'),
    path('client-records/', views.warehouse_client_records, name='warehouse_client_records'),
    path('received_requests/', views.warehouse_received_requests, name='warehouse_received_requests'),
    path('sent_requests/', views.warehouse_sent_requests, name='warehouse_sent_requests'),
    path('settings/', views.warehouse_settings, name='warehouse_settings'),
    path('invoice/', views.warehouse_invoice, name='warehouse_invoice'),
    path('restock-inventory/<int:item_id>/', views.restock_inventory, name='warehouse_restock_inventory'),
    
    # API endpoints
    path('api/create-order/', views.create_order, name='create_order'),
    path('api/get-item-details/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('api/update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('api/update-payment/', views.update_payment, name='update_payment'),
    path('api/cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('api/send-to-delivery/', views.send_to_delivery, name='send_to_delivery'),
    path('api/client-orders/<int:client_id>/', views.get_client_orders, name='get_client_orders'),
    path('api/client-invoices/<int:client_id>/', views.get_client_invoices, name='get_client_invoices'),
]
