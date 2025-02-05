from django.contrib import admin
from django import forms
from .models import Address
from django.core.exceptions import ValidationError

# Custom form for Address and ShippingAddress models to validate latitude and longitude
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


# Custom admin for Address
class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ('apartment', 'home', 'street')
    search_fields = ('street',)




# Register models with the admin panel
admin.site.register(Address, AddressAdmin)