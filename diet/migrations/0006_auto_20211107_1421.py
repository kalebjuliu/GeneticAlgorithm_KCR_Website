# Generated by Django 3.2.9 on 2021-11-07 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0005_userbmi_bmi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbmi',
            name='bmi',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userbmi',
            name='bmr',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
