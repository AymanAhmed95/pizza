# Generated by Django 3.0 on 2020-07-12 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaApp', '0006_auto_20200712_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizzasize',
            name='pizzaSize',
        ),
        migrations.AddField(
            model_name='pizza',
            name='pizza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pizzaApp.PizzaSize'),
        ),
    ]