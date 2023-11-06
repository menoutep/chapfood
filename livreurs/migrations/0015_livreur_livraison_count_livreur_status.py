# Generated by Django 4.2.5 on 2023-11-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livreurs', '0014_rename_commande_livraison_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='livreur',
            name='livraison_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='livreur',
            name='status',
            field=models.CharField(choices=[('en_attente', 'En attente'), ('en_livraison', 'En livraison')], default='en_attente', max_length=20),
        ),
    ]
