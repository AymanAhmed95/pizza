# Generated by Django 3.0 on 2020-07-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaApp', '0009_auto_20200712_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pizza',
            field=models.ManyToManyField(related_name='orderPizza', through='pizzaApp.OrderPizzaRel', to='pizzaApp.Pizza'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='pizzaSize',
            field=models.ManyToManyField(related_name='PizzaSizeRel', through='pizzaApp.PizzaSizeRel', to='pizzaApp.PizzaSize'),
        ),
    ]