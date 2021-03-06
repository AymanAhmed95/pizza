# Generated by Django 3.0 on 2020-07-13 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaApp', '0013_auto_20200712_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pizza',
            field=models.ManyToManyField(related_name='orderPizza', through='pizzaApp.OrderPizzaRel', to='pizzaApp.Pizza'),
        ),
        migrations.AlterField(
            model_name='orderpizzarel',
            name='pizza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pizzaApp.Pizza'),
        ),
    ]
