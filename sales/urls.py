from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.sales_base, name='sales_base'),
    path('dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path('inventory/', views.sales_inventory, name='sales_inventory'),
    path('forecasting/', views.sales_forecasting, name='sales_forecasting'),
    path('equipment/', views.sales_equipment, name='sales_equipment'),
    path('orders/', views.sales_orders, name='sales_orders'),
    path('invoicing/', views.sales_invoicing, name='sales_invoicing'),
    path('client_records/', views.sales_client_records, name='sales_client_records'),
    path('received_requests/', views.sales_received_requests, name='sales_received_requests'),
    path('sent_requests/', views.sales_sent_requests, name='sales_sent_requests'),
    path('restock-inventory/<int:item_id>/', views.sales_restock_inventory, name='sales_restock_inventory'),
    path('settings/', views.sales_settings, name='sales_settings'),
    
    # New URLs for sales orders
    path('create-order/', views.create_sales_order, name='create_sales_order'),
    path('get-item-details/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('update-order/<int:order_id>/', views.update_sales_order, name='update_sales_order'),
    path('get-order-details/<int:order_id>/', views.get_order_details, name='get_order_details'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('update-payment/', views.update_payment, name='update_payment'),
    path('check-overdue/', views.check_overdue, name='check_overdue'),
    path('create-pdi-request/', views.create_pdi_request, name='create_pdi_request'),
    path('update-request-notes/', views.update_request_notes, name='update_request_notes'),
    path('api/client-orders/<int:client_id>/', views.client_orders, name='client_orders'),
    path('api/client-invoices/<int:client_id>/', views.client_invoices, name='client_invoices'),
    path('api/create-order/', views.create_sales_order, name='api_create_order'),
]
                    