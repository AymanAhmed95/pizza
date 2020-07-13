from django.test import TestCase

# Create your tests here.
from .constants import ORDER_STATUS_PENDING
from .models import Order, Customer, Pizza, OrderPizzaRel


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


def get_test_user():
    return Customer.objects.first()


def get_test_pizza():
    return Pizza.objects.first()
