# Generated by Django 4.2 on 2024-10-25 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrévisionPrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_prevision', models.DateField()),
                ('prix_prevu', models.DecimalField(decimal_places=2, max_digits=10)),
                ('confiance', models.DecimalField(decimal_places=2, max_digits=5)),
                ('methode', models.CharField(max_length=100)),
            ],
        ),
    ]
