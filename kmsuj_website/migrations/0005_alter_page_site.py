# Generated by Django 3.2.9 on 2022-05-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kmsuj_website', '0004_auto_20220429_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='site',
            field=models.CharField(choices=[('WARSZTATY', 'WARSZTATY'), ('KMSUJ', 'KMS UJ'), ('OSSM', 'OSSM')], default='KMSUJ', max_length=9),
        ),
    ]