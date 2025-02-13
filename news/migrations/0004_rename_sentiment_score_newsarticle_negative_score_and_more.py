# Generated by Django 5.1.2 on 2024-10-29 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_newsarticle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsarticle',
            old_name='sentiment_score',
            new_name='negative_score',
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='neutral_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='positive_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='sentiment_label',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
