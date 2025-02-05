# Generated by Django 5.1.3 on 2025-01-27 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название филиала')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название филиала')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Название филиала')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Название филиала')),
                ('working_days', models.CharField(max_length=255, verbose_name='Рабочие дни')),
                ('working_days_ru', models.CharField(max_length=255, null=True, verbose_name='Рабочие дни')),
                ('working_days_uz', models.CharField(max_length=255, null=True, verbose_name='Рабочие дни')),
                ('working_days_en', models.CharField(max_length=255, null=True, verbose_name='Рабочие дни')),
                ('working_time', models.CharField(max_length=255, verbose_name='Рабочее время')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('address_ru', models.CharField(max_length=255, null=True, verbose_name='Адрес')),
                ('address_uz', models.CharField(max_length=255, null=True, verbose_name='Адрес')),
                ('address_en', models.CharField(max_length=255, null=True, verbose_name='Адрес')),
                ('address_url', models.URLField(verbose_name='Ссылка адреса')),
                ('latitude', models.CharField(max_length=50, verbose_name='Широта')),
                ('longitude', models.CharField(max_length=50, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
        migrations.CreateModel(
            name='IKPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ikpu', models.TextField(verbose_name='ИКПУ')),
            ],
        ),
        migrations.CreateModel(
            name='LoyaltyCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(editable=False, max_length=16, unique=True, verbose_name='Номер карты')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Баланс')),
                ('status', models.CharField(choices=[('active', 'Активна'), ('inactive', 'Неактивна'), ('blocked', 'Заблокирована')], default='active', max_length=10, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Лояльная карта',
                'verbose_name_plural': 'Лояльные карты',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название продукта')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Название продукта')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Название продукта')),
                ('description', models.TextField(verbose_name='Описание продукта')),
                ('description_ru', models.TextField(null=True, verbose_name='Описание продукта')),
                ('description_uz', models.TextField(null=True, verbose_name='Описание продукта')),
                ('description_en', models.TextField(null=True, verbose_name='Описание продукта')),
                ('packing_code', models.CharField(max_length=255, verbose_name='Код упаковки')),
                ('slug', models.SlugField(editable=False, unique=True, verbose_name='Slug')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Изображение продукта')),
                ('is_active', models.BooleanField(verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SizeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50, verbose_name='Size')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('unit', models.CharField(choices=[('ml', 'Миллилитр'), ('g', 'Грамм')], default='g', max_length=2, verbose_name='Unit of measurement')),
                ('unit_ru', models.CharField(choices=[('ml', 'Миллилитр'), ('g', 'Грамм')], default='g', max_length=2, null=True, verbose_name='Unit of measurement')),
                ('unit_uz', models.CharField(choices=[('ml', 'Миллилитр'), ('g', 'Грамм')], default='g', max_length=2, null=True, verbose_name='Unit of measurement')),
                ('unit_en', models.CharField(choices=[('ml', 'Миллилитр'), ('g', 'Грамм')], default='g', max_length=2, null=True, verbose_name='Unit of measurement')),
            ],
            options={
                'verbose_name': 'Size Option',
                'verbose_name_plural': 'Size Options',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Syrup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Сироп',
                'verbose_name_plural': 'Сиропы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название категории')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Название категории')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Название категории')),
                ('slug', models.SlugField(editable=False, null=True, unique=True, verbose_name='Slug категории')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='Coffeeroom.branch', verbose_name='Филиал')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]
