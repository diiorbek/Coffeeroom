# Generated by Django 5.1.3 on 2025-02-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_orderproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='syrup',
        ),
        migrations.RemoveField(
            model_name='order',
            name='loyalty_card',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Ожидает'), ('shipped', 'Отправлен'), ('delivered', 'Доставлен'), ('cancelled', 'Отменён')], default='pending', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Общая сумма'),
        ),
    ]
