# Generated by Django 5.0.3 on 2024-04-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advapp', '0003_category_alter_advert_icon_alter_advert_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='category'),
        ),
    ]