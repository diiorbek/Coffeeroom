from django.core.exceptions import ValidationError
from django.db import models
from account.models import User
import re
import random
from django.utils.text import slugify
from unidecode import unidecode
from django.utils.translation import gettext_lazy as _

product_count = 1
category_count = 1


LAT_LON_REGEX = r"^(-?\d{1,2}(\.\d+)?),\s*(-?\d{1,3}(\.\d+)?)$"

class Branch(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название филиала")
    working_days = models.CharField(max_length=255, verbose_name="Рабочие дни")
    working_time = models.CharField(max_length=255, verbose_name="Рабочее время")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    address_url = models.URLField(verbose_name="Ссылка адреса")
    latitude = models.CharField(max_length=50, verbose_name="Широта")
    longitude = models.CharField(max_length=50, verbose_name="Долгота")

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def clean(self):
        if not self.working_days:
            raise ValidationError("Рабочие дни не могут быть пустыми.")
        if not self.working_time:
            raise ValidationError("Рабочее время не может быть пустым.")

        lat_lon_validator = re.compile(LAT_LON_REGEX)

        if not lat_lon_validator.match(f"{self.latitude},{self.longitude}"):
            raise ValidationError("Широта и долгота должны быть в формате '-90.0, 180.0'.")
        
        try:
            lat = float(self.latitude)
            lon = float(self.longitude)
            if not (-90 <= lat <= 90):
                raise ValidationError("Широта должна быть в диапазоне от -90 до 90.")
            if not (-180 <= lon <= 180):
                raise ValidationError("Долгота должна быть в диапазоне от -180 до 180.")
        except ValueError:
            raise ValidationError("Широта и долгота должны быть числами.")
    
    def __str__(self):
        return self.title


from django.db.models.signals import pre_save
from django.utils.crypto import get_random_string

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название категории")
    branch = models.ForeignKey(
        "Branch",
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Филиал"
    )
    slug = models.SlugField(unique=True, editable=False, verbose_name="Slug категории", null=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title
    
def generate_unique_slug_category(instance):
    """ Unikal slug generatsiya qiluvchi funksiya """
    global category_count  # Global o'zgaruvchini chaqiramiz
    base_slug = slugify(unidecode(instance.title), allow_unicode=True)
    slug = base_slug
    while Category.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{category_count}"
        category_count += 1  # O'zgaruvchini yangilaymiz
    return slug

def generate_unique_slug_product(instance):
    """ Unikal slug generatsiya qiluvchi funksiya """
    global product_count  # Global o'zgaruvchini chaqiramiz
    base_slug = slugify(unidecode(instance.title), allow_unicode=True)
    slug = base_slug
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{product_count}"
        product_count += 1  # O'zgaruvchini yangilaymiz
    return slug


def category_pre_save(sender, instance, *args, **kwargs):
    """ Model saqlashdan oldin slugni avtomatik yaratadi """
    if not instance.slug:
        instance.slug = generate_unique_slug_category(instance)

pre_save.connect(category_pre_save, sender=Category)


class Product(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название продукта"
    )
    description = models.TextField(
        verbose_name="Описание продукта"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    packing_code = models.CharField(
        max_length=255,
        verbose_name="Код упаковки",
        unique=True
    )
    ikpu = models.ForeignKey(
        "IKPU",
        on_delete=models.CASCADE,
        verbose_name="ИКПУ"
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        verbose_name="Slug"
    )

    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение продукта"
    )

    is_active = models.BooleanField(
        verbose_name="Активен"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["title"]


    def clean(self):
        if not self.title:
            raise ValidationError("Название продукта не может быть пустым.")
        if not self.category:
            raise ValidationError("Продукту должна быть назначена категория.")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.branch = self.category.branch
        super().save(*args, **kwargs)
    
    def __str__(self):

        return self.title

def product_pre_save(sender, instance, *args, **kwargs):
    """ Model saqlashdan oldin slugni avtomatik yaratadi """
    if not instance.slug:
        instance.slug = generate_unique_slug_product(instance)

pre_save.connect(product_pre_save, sender=Product)


class SizeOption(models.Model):
    UNIT_CHOICES = [
        ("ml", _("Миллилитр")),  # Локализованные значения
        ("g", _("Грамм")),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="size_options",
        verbose_name=_("Product")
    )
    size = models.CharField(max_length=50, verbose_name=_("Size"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        default="g",
        verbose_name=_("Unit of measurement")
    )

    class Meta:
        verbose_name = _("Size Option")
        verbose_name_plural = _("Size Options")
        ordering = ["price"]

    def __str__(self):
        return self.size

class LoyaltyCard(models.Model):
    CARD_STATUS_CHOICES = [
        ('active', 'Активна'),
        ('inactive', 'Неактивна'),
        ('blocked', 'Заблокирована'),
    ]

    card_number = models.CharField(
        max_length=16, 
        unique=True, 
        editable=False,  # Делает поле недоступным для редактирования в админке и формах
        verbose_name="Номер карты"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='loyalty_cards',
        verbose_name="Владелец"
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Баланс"
    )
    status = models.CharField(
        max_length=10,
        choices=CARD_STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Лояльная карта"
        verbose_name_plural = "Лояльные карты"

    def __str__(self):
        return self.card_number

    def add_points(self, amount):
        if self.status == 'active':
            self.balance += amount
            self.save()

    def redeem_points(self, amount):
        if self.status == 'active' and self.balance >= amount:
            self.balance -= amount
            self.save()

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.card_number = self.generate_unique_card_number()
        super().save(*args, **kwargs)

    def generate_unique_card_number(self):
        while True:
            number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            if not LoyaltyCard.objects.filter(card_number=number).exists():
                return number
                
class Syrup(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    products = models.ManyToManyField(
        "Coffeeroom.Product",
        related_name="syrups",
        verbose_name="Продукты"
    )

    class Meta:
        verbose_name = "Сироп"
        verbose_name_plural = "Сиропы"

    def clean(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной.")

    def __str__(self):
        return self.title

class IKPU(models.Model):
    ikpu = models.TextField(verbose_name="ИКПУ")
    
    class Meta:
        verbose_name = "ИКПУ"
        verbose_name_plural = "ИКПУ"
    
    def __str__(self):
        return self.ikpu
    