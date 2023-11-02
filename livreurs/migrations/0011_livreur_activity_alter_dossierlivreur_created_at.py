# Generated by Django 4.2.5 on 2023-10-31 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livreurs', '0010_dossierlivreur_refuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livreur',
            name='activity',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dossierlivreur',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 31, 20, 20, 20, 143193, tzinfo=datetime.timezone.utc)),
        ),
    ]
