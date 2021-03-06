# Generated by Django 3.0 on 2020-07-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaApp', '0002_auto_20200712_1048'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductImage',
            new_name='PizzaImage',
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.TextField(choices=[('Pending', 'Pending'), ('Work on', 'Work on'), ('On delivery', 'On delivery'), ('Delivered', 'Delivered')], default='Pending'),
        ),
        migrations.AddField(
            model_name='orderpizzarel',
            name='pizzasNumber',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
