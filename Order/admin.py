from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Cart, CartItem, PaymentMethod, Order, OrderProduct


# Custom form for Cart model
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get('total_amount')
        if total_amount is not None and total_amount < 0:
            raise ValidationError("Total amount cannot be negative.")
        return cleaned_data


# Custom form for CartItem model
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return cleaned_data


# Custom form for PaymentMethod model
class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('method')
        if not method:
            raise ValidationError("Payment method name cannot be empty.")
        return cleaned_data


# Custom form for Order model
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get('total_amount')
        if total_amount is not None and total_amount <= 0:
            raise ValidationError("Total amount must be greater than zero.")
        return cleaned_data



# Custom admin for Cart
class CartAdmin(admin.ModelAdmin):
    form = CartForm
    list_display = ('user', 'session_key', 'total_amount', 'created_at', 'updated_at')
    search_fields = ('user__phone_number', 'session_key')


# Custom admin for CartItem
class CartItemAdmin(admin.ModelAdmin):
    form = CartItemForm
    list_display = ('cart', 'product', 'quantity', 'added_at', 'get_syrup')
    search_fields = ('cart__session_key', 'product__title')

    def get_syrup(self, obj):
        return ", ".join([syrup.title for syrup in obj.syrups.all()])
    get_syrup.short_description = "Сиропы"


# Custom admin for PaymentMethod
class PaymentMethodAdmin(admin.ModelAdmin):
    form = PaymentMethodForm
    list_display = ('method',)
    search_fields = ('method',)


# Custom admin for Order
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('customer', 'total_amount', 'status', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'id')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Order, OrderAdmin)