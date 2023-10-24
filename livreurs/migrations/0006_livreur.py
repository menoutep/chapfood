# Generated by Django 4.2.5 on 2023-10-23 17:05

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0011_category_image_order_is_piece_order_monnaie'),
        ('livreurs', '0005_delete_livreur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livreur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('position', models.TextField()),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.order')),
                ('dossier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='livreurs.dossierlivreur')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
