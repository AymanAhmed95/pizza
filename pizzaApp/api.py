from django.core.exceptions import ObjectDoesNotExist

from rest_framework import routers
from .views import CustomerViewSet, PizzaViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'pizza', PizzaViewSet)
router.register(r'orders', OrderViewSet)
