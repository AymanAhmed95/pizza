# Create your tests here.
from rest_framework.status import HTTP_200_OK

from .constants import ORDER_STATUS_PENDING
from .models import Order, Customer, Pizza, OrderPizzaRel
from django.test import TestCase, Client
from pprint import pprint

from .serializers import OrderSerializer
from rest_framework.test import APIRequestFactory, APITestCase

from .views import OrderViewSet


class OrderTest(TestCase):

    def test_add_order(self):
        order = Order()
        order.state = ORDER_STATUS_PENDING
        order.delivery = 17.0
        test_customer = get_test_user()
        order.customer = test_customer
        order.save()
        order_pizza = OrderPizzaRel()
        order_pizza.pizza = get_test_pizza()
        order_pizza.order = order
        order_pizza.pizzasNumber = 27
        order_pizza.save()

        db_order = Order.objects.latest('created')
        self.assertEqual(order.id, db_order.id)


class ApiTest(APITestCase):
    def test_get_orders_api(self):
        factory = APIRequestFactory()
        orderView = OrderViewSet.as_view({'get': 'list'})
        request = factory.get(path='/orders', content_type='application/json')
        orders = orderView(request)
        self.assertEqual(orders.status_code, HTTP_200_OK)
        self.assertEqual(orders.data, OrderSerializer(Order.objects.all(), many=True).data)


def get_test_user():
    return Customer.objects.first()


def get_test_pizza():
    return Pizza.objects.first()
