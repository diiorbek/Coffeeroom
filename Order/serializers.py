from rest_framework import serializers
from .models import CartItem, PaymentMethod, Order, Cart
from Coffeeroom.serializers import ProductSerializer, SyrupSerializer  # Добавляем SyrupSerializer
from common.serializers import AddressSerializer
from common.models import Address


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    syrups = SyrupSerializer(many=True)  # Здесь нужно изменить на SyrupSerializer, а не StringRelatedField

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'syrups']  # Исправлено на syrups


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, source='cartitem_set')
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_amount']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'method']


class OrderSerializer(serializers.ModelSerializer):
    order_products = CartItemSerializer(many=True, source='cart.cartitem_set')  # Используем CartItemSerializer
    customer = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer()  # Используем сериализатор для Address
    payment_method = serializers.SerializerMethodField()

    def get_payment_method(self, obj):
        return obj.payment_method.method
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'created_at', 
            'address', 
            'payment_method', 
            'status', 
            'total_amount', 
            'order_products',
            'customer'
        ]
        
        read_only_fields = ['id', 'created_at', 'status', 'total_amount', 'order_products', 'customer']


class OrderCreateSerializer(serializers.Serializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    payment_method = serializers.PrimaryKeyRelatedField(queryset=PaymentMethod.objects.all())

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Аутентификация обязательна для оформления заказа.")
        user = request.user
        address = validated_data['address']
        payment_method = validated_data['payment_method']

        order = Order.create_order_from_cart(user, address, payment_method)
        return order

    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data
