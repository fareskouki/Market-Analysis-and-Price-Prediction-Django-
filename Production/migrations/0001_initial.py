# Generated by Django 3.1.7 on 2024-10-26 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Climat', '0003_donneeclimatique_produit_marche'),
        ('marche', '0005_auto_20241026_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.FloatField()),
                ('date', models.DateField()),
                ('region', models.CharField(max_length=255)),
                ('donnees_climatiques', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productions', to='Climat.donneeclimatique')),
                ('produit_marche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productions', to='marche.donneemarche')),
            ],
        ),
    ]
