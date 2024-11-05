# Generated by Django 3.1.7 on 2024-10-26 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marche', '0005_auto_20241026_1412'),
        ('Climat', '0002_auto_20241025_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='donneeclimatique',
            name='produit_marche',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='donnees_climatiques', to='marche.donneemarche'),
            preserve_default=False,
        ),
    ]
