from django.core.exceptions import ValidationError
from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Улица")
    apartment = models.CharField(max_length=255, blank=True, null=True, verbose_name="Квартира")
    home = models.CharField(max_length=255, blank=True, null=True, verbose_name="Дом")
    orientation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ориентация")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
    
    def __str__(self):
        return self.street