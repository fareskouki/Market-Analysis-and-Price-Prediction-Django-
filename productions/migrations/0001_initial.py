# Generated by Django 5.1.2 on 2024-10-29 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('denrees_agricoles', '0003_delete_production'),
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('year', models.IntegerField()),
                ('description', models.TextField()),
                ('denree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productions', to='denrees_agricoles.denreesagricoles')),
            ],
        ),
    ]
