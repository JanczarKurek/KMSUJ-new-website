# Generated by Django 3.2.9 on 2022-03-19 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kmsuj_website', '0002_page_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='site',
            field=models.CharField(choices=[('KMSUJ', 'KMS UJ'), ('OSSM', 'OSSM')], default='KMSUJ', max_length=5),
        ),
    ]