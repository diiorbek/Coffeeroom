# Generated by Django 5.1.3 on 2025-02-20 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coffeeroom', '0004_alter_product_packing_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True, unique=True, verbose_name='Slug категории'),
        ),
    ]
