from django.core.exceptions import ObjectDoesNotExist

from .models import *
from rest_framework import serializers

from .constants import ORDER_STATUS_PENDING, ORDER_STATUS_WORK_ON


class PizzaSizSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaSize
        fields = '__all__'


class PizzaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaImage
        fields = ['id', 'image', 'created']


class PizzaSerializer(serializers.ModelSerializer):
    """ Pizza M2M PizzaSize through model serializer"""

    images = PizzaImageSerializer(many=True, read_only=True)
    pizzaSize = PizzaSizSerializer(many=True, read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Pizza
        fields = ['id', 'title', 'description', 'created', 'updated', 'pizzaSize', 'images']
        # make title description not required so as to we can add pizza to order  with id only
        extra_kwargs = {'title': {'required': False}, 'description': {'required': False}, }


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address']
        # make all fields not required to enable adding new customer with the order or by its id if exists
        extra_kwargs = {'id': {'required': False},
                        'phone': {'required': False},
                        'address': {'required': False},
                        'name': {'required': False}, }


class OrderPizzaRelSerializer(serializers.ModelSerializer):
    """ Order M2M Pizza through model serializer"""

    class Meta:
        model = OrderPizzaRel
        fields = serializers.ALL_FIELDS


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    pizza = OrderPizzaRelSerializer(many=True)
    # to retrieve records from through model
    orderPizza = serializers.SerializerMethodField(method_name='get_order_pizza')

    class Meta:
        model = Order
        fields = ('state', 'customer', 'delivery', 'orderPizza', 'pizza', 'created', 'updated')

    # method for getting through model records using it order.id
    def get_order_pizza(self, order):
        if isinstance(order, Order):
            orderPizza = order.pizza.through.objects.filter(order_id=order.id)
            return [OrderPizzaRelSerializer().to_representation(pizza) for pizza in
                    orderPizza]

    # overriding serializer create method because of many to many relation with through model
    def create(self, validated_data):
        order = Order()
        order.state = validated_data['state']
        order.delivery = validated_data['delivery']
        if 'id' in validated_data['customer']:
            try:
                customer = Customer.objects.get(id=validated_data['customer']['id'])
                order.customer = customer
                order.save()
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    {"error": "customer with id " + str(validated_data['customer']['id']) + " does not exist"})
        else:
            if all(field in validated_data['customer'] for field in ['name', 'phone', 'address']):
                customer = Customer()
                customer.name = validated_data['customer']['name']
                customer.phone = validated_data['customer']['phone']
                customer.address = validated_data['customer']['address']
                customer.save()
                order.customer = customer
                order.save()
            else:
                raise serializers.ValidationError(
                    {"error": "in-valid customer information"})

        if len(validated_data['pizza']):
            order.save()
            for pizzaId in validated_data['pizza']:
                try:
                    pizza = pizzaId['pizza']
                    orderPizzaRel = OrderPizzaRel()
                    orderPizzaRel.order = order
                    orderPizzaRel.pizza = pizza
                    orderPizzaRel.pizzasNumber = pizzaId['pizzasNumber']
                    orderPizzaRel.save()
                    # order.pizza.add(pizza)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(
                        {"error": "Pizza with id " + str(pizzaId['pizza']['id']) + " does not exist"})
            order.save()
        return order

    # overriding serializer Update method because of many to many relation with through model
    def update(self, instance, validated_data):
        instance.state = validated_data['state']
        if validated_data['state'] in [ORDER_STATUS_PENDING, ORDER_STATUS_WORK_ON]:
            instance.delivery = validated_data['delivery']
            if len(validated_data['pizza']):
                instance.pizza.clear()
                for pizzaId in validated_data['pizza']:
                    try:
                        pizza = pizzaId['pizza']
                        orderPizzaRel = OrderPizzaRel()
                        orderPizzaRel.order = instance
                        orderPizzaRel.pizza = pizza
                        orderPizzaRel.pizzasNumber = pizzaId['pizzasNumber']
                        orderPizzaRel.save()
                        # order.pizza.add(pizza)
                    except ObjectDoesNotExist:
                        raise serializers.ValidationError(
                            {"error": "Pizza with id " + str(pizzaId['pizza']['id']) + " does not exist"})
                instance.save()
        return instance
