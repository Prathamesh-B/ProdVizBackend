# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionLineViewSet, TagViewSet, AlertViewSet, LogView, MachinePerformanceView

router = DefaultRouter()
router.register(r'productionlines', ProductionLineViewSet)
router.register(r'tags', TagViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logs/', LogView.as_view(), name='logs'),
    path('machine-performance/', MachinePerformanceView.as_view(), name='machine-performance'),
]
