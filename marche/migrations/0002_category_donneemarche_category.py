# Generated by Django 4.2 on 2024-10-26 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marche', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='donneemarche',
            name='category',
            field=models.ForeignKey(default=0.001284584980237154, on_delete=django.db.models.deletion.CASCADE, related_name='donnees_marche', to='marche.category'),
            preserve_default=False,
        ),
    ]
