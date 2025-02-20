from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .models import Cart, Order
from .serializers import CartSerializer, OrderSerializer, OrderCreateSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            raise NotFound(detail="Cart matching query does not exist.")


class ActiveOrdersView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, user_id):
        active_orders = Order.objects.filter(customer__id=user_id, status='pending')
        
        if not active_orders.exists():
            raise NotFound(detail="No active orders found for this user.")
        
        serializer = OrderSerializer(active_orders, many=True)
        return Response(serializer.data)

class HistoryOrdersView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, user_id):
        history_orders = Order.objects.filter(customer__id=user_id, status__in=['shipped', 'delivered', 'canceled'])
    
     
        if not history_orders.exists():
            raise NotFound(detail="No active orders found for this user.")
        
        serializer = OrderSerializer(history_orders, many=True)
        return Response(serializer.data)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order, context={'request': request}).data)
