# Generated by Django 4.2.4 on 2023-10-17 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('road_bible', '0005_customroads'),
    ]

    operations = [
        migrations.AddField(
            model_name='customroads',
            name='creator',
            field=models.CharField(default='N/a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customroads',
            name='title',
            field=models.CharField(default='N/a', max_length=255),
            preserve_default=False,
        ),
    ]