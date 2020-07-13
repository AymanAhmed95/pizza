from django.db import models
from .util import get_images_path
from .constants import ORDER_STATUS_PENDING, ORDER_STATUS_WORK_ON, ORDER_STATUS_ON_DELIVERY, ORDER_STATUS_DELIVERED
from django.utils.translation import gettext_lazy as _


class Pizza(models.Model):
    """
     M2M with order
     M2M with pizzaSize
     pizza price is variant based on pizza size
    """
    title = models.CharField(max_length=255)
    description = models.TextField()  # for simplicity gradients goes here
    pizzaSize = models.ManyToManyField('PizzaSize', related_name='PizzaSizeRel', through='PizzaSizeRel')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class PizzaSize(models.Model):
    """ M2M with pizza"""
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class PizzaSizeRel(models.Model):
    """ Pizza and Pizza size through model and it holds the price"""
    pizza = models.ForeignKey('Pizza', null=True, on_delete=models.SET_NULL)
    pizzaSize = models.ForeignKey('PizzaSize', null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class PizzaImage(models.Model):
    pizza = models.ForeignKey('Pizza', related_name="images", default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_images_path)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Customer(models.Model):
    """holds pizza customer base data"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Order(models.Model):
    """
     M2M with pizza
     M21 with customer
     hold order info and status
     status are pending,work on,on delivery,delivered
    """

    class OrderStatus(models.TextChoices):
        PENDING = ORDER_STATUS_PENDING, _(ORDER_STATUS_PENDING)
        WORK_ON = ORDER_STATUS_WORK_ON, _(ORDER_STATUS_WORK_ON)
        ON_DELIVERY = ORDER_STATUS_ON_DELIVERY, _(ORDER_STATUS_ON_DELIVERY)
        DELIVERED = ORDER_STATUS_DELIVERED, _(ORDER_STATUS_DELIVERED)

    state = models.TextField(choices=OrderStatus.choices, default=OrderStatus.PENDING)

    pizza = models.ManyToManyField('Pizza', related_name='orderPizza',through='OrderPizzaRel',
                                   through_fields=('order', 'pizza'))

    customer = models.ForeignKey('Customer', null=True, on_delete=models.SET_NULL)
    delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class OrderPizzaRel(models.Model):
    """
    Order pizza relation through model
    holds number of pizzas 
    """
    order = models.ForeignKey('Order', null=True, on_delete=models.SET_NULL)
    pizza = models.ForeignKey('Pizza', null=True, on_delete=models.SET_NULL)
    pizzasNumber = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
