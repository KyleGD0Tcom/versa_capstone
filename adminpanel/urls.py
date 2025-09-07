from django.urls import path
from . import views


urlpatterns = [
    path('base/', views.admin_base, name='adminpanel_base'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('user_management/', views.user_management_view, name='user_management'),
    path('department/', views.department_view, name='department'),
    path('invoicing/', views.Operations_invoicing_view, name='operations_invoicing'),
    path('inventory/', views.Operations_inventory_view, name='operations_inventory'),
    path('forecast/', views.Operations_forecast_view, name='operations_forecast'),
    path('sales&Orders/', views.SalesAndOrders_view, name='operations_salesAndOrders'),
    path('motorpool/', views.motorpool_view, name='operations_motorpool'),
    path('aftersales/', views.Aftersales_view, name='operations_aftersales'),
    path('delivery&Tracking/', views.Delivery_Tracking_view, name='delivery_tracking'),
    path('risk&Anomalies/', views.RiskAndAnomalies_view, name='riskAndAnomalies'),
    path('audit trail/', views.AuditTrail_view, name='auditTrail'),
    path('settings/', views.Settings_view, name='settings'),
    path('notifications/', views.Notifications_view, name='notifications'),
    path('update-request-notes/', views.admin_update_request_notes, name='admin_update_request_notes'),
    path('api/orders-feed/', views.orders_feed, name='admin_orders_feed'),
]
