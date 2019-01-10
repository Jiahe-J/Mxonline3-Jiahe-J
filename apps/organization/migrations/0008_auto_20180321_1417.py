# Generated by Django 2.0.1 on 2018-03-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20180316_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, upload_to='org/%Y/%m', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='著名机构', max_length=10, verbose_name='机构标签'),
        ),
    ]
