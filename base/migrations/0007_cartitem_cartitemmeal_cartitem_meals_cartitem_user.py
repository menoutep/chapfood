# Generated by Django 4.2.5 on 2023-09-25 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('base', '0006_delete_commande'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CartItemMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.cartitem')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.meal')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='meals',
            field=models.ManyToManyField(through='base.CartItemMeal', to='base.meal'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser'),
        ),
    ]
