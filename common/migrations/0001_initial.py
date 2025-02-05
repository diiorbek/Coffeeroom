# Generated by Django 5.1.3 on 2025-01-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('street_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('street_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('street_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('apartment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Квартира')),
                ('apartment_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Квартира')),
                ('apartment_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Квартира')),
                ('apartment_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Квартира')),
                ('home', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дом')),
                ('home_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дом')),
                ('home_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дом')),
                ('home_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дом')),
                ('orientation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ориентация')),
                ('orientation_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ориентация')),
                ('orientation_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ориентация')),
                ('orientation_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ориентация')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
    ]
