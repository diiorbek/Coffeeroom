from django.core.exceptions import ValidationError
from django.db import models
from Coffeeroom.models import LoyaltyCard, Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from account.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    session_key = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ключ сессии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Общая сумма"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def clean(self):
        if self.total_amount < 0:
            raise ValidationError("Общая сумма не может быть отрицательной.")

    def update_total_amount(self):
        total = Decimal('0.00')
        for item in self.cartitem_set.all():
            if item.size_option:
                total += item.size_option.price * item.quantity

            if item.syrups.exists():
                for syrup in item.syrups.all():
                    total += syrup.price * item.quantity

        # Логируем итоговую сумму для отладки
        print(f"Обновленная общая сумма корзины: {total}")

        self.total_amount = total
        self.save(update_fields=['total_amount'])

        # Обновляем все заказы, связанные с корзиной
        for order in self.order_set.all():
            order.total_amount = self.total_amount
            order.save()

    def __str__(self):
        return f"{self.user} - {self.session_key}"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    size_option = models.ForeignKey(
        "Coffeeroom.SizeOption",
        on_delete=models.CASCADE,
        verbose_name="Опция размера"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    syrups = models.ManyToManyField('Coffeeroom.Syrup', blank=True, verbose_name="Сиропы")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Количество должно быть больше нуля.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Пересчитываем общую сумму корзины после сохранения элемента
        self.cart.update_total_amount()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Пересчитываем общую сумму корзины после удаления элемента
        self.cart.update_total_amount()



class PaymentMethod(models.Model):
    method = models.CharField(max_length=50, unique=True, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"

    def __str__(self):
        return self.method


class Order(models.Model):
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Ожидает'),
        (SHIPPED, 'Отправлен'),
        (DELIVERED, 'Доставлен'),
        (CANCELLED, 'Отменён'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    address = models.ForeignKey("common.Address", on_delete=models.CASCADE, verbose_name="Адрес доставки")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, verbose_name="Способ оплаты")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name="Общая сумма заказа",
        editable=False  
    )
    status = models.CharField(max_length=50, verbose_name="Статус", choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        # Перед сохранением обновляем сумму заказа на основе суммы корзины
        self.total_amount = self.cart.total_amount
        super().save(*args, **kwargs)

    @classmethod
    def create_order_from_cart(cls, user, address, payment_method):
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.cartitem_set.exists():
            raise ValidationError("Корзина пуста. Добавьте товары перед оформлением заказа.")

        cart.update_total_amount()

        print(f"Общая сумма корзины перед созданием заказа: {cart.total_amount}")

        # Создаем заказ, поле total_amount будет установлено через save()
        order = cls.objects.create(
            customer=user,
            address=address,
            payment_method=payment_method,
            cart=cart
        )

        print(f"Созданный заказ с суммой: {order.total_amount}")

        # Создаем связанные товары в заказе
        for cart_item in cart.cartitem_set.all():
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        cart.cartitem_set.all().delete()
        cart.update_total_amount()

        return order





class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.title} в заказе {self.order.id}'
