from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart, Order

@receiver(post_save, sender=Cart)
def update_orders_total_amount(sender, instance, **kwargs):
    for order in instance.order_set.all(): 
        order.total_amount = instance.total_amount  
        order.save()