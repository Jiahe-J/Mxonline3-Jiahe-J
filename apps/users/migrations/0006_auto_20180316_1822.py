# Generated by Django 2.0.1 on 2018-03-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180313_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, upload_to='banner/%Y/%m', verbose_name='轮播图'),
        ),
    ]
