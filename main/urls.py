# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionLineViewSet, TagViewSet, AlertView, LogView, MachinePerformanceView, ControlPanelDataView

router = DefaultRouter()
router.register(r'productionlines', ProductionLineViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logs/', LogView.as_view(), name='logs'),
    path('machine-performance/', MachinePerformanceView.as_view(), name='machine-performance'),
    path('alerts/', AlertView.as_view(), name='alert-list'),
    path('alerts/<int:pk>', AlertView.as_view(), name='alert-detail'),
    path('control-panel-data/', ControlPanelDataView.as_view(), name='control-panel-data'),
]
