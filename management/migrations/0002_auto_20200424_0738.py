# Generated by Django 3.0.5 on 2020-04-24 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='prix',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantite',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
