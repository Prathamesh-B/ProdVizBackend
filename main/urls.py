from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AlertView,
    AuthRoleViewSet,
    AuthUserViewSet,
    BlockViewSet,
    ControlPanelDataView,
    DaqLogView,
    IncidentTransactionViewSet,
    IncidentViewSet,
    LineViewSet,
    MachinePerformanceView,
    MachineViewSet,
    PlantViewSet,
    ProductionLineDetailView,
    ProductionMetricsView,
    SensorTagTypeViewSet,
    SensorTagViewSet,
)

router = DefaultRouter()
router.register(r'plants', PlantViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'lines', LineViewSet)
router.register(r'sensortags', SensorTagViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'users', AuthUserViewSet)
router.register(r'roles', AuthRoleViewSet)
router.register(r'tag-types', SensorTagTypeViewSet)
router.register(r'incidents', IncidentViewSet)
router.register(r'incident-transactions', IncidentTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('alerts/', AlertView.as_view(), name='alerts'),
    path('daqlogs/', DaqLogView.as_view(), name='daqlogs'),
    path('machine-performance/', MachinePerformanceView.as_view(), name='machine-performance'),
    path('production-line-details/', ProductionLineDetailView.as_view(), name='production-line-details'),
    path('production-metrics/', ProductionMetricsView.as_view(), name='production-metrics'),
    path('control-panel-data/', ControlPanelDataView.as_view(), name='control-panel-data'),
]