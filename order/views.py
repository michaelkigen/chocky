from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,viewsets
from .models import CartItem,Cart, Order,OrderedItem
from rest_framework.permissions import IsAuthenticated
from .token_auth import JWTAuthentication
from .serializers import (
     CartSerializer,AddCartItemSerializer,Update_cart_serializer,CartItemSerializer,Order_Serializer,OrderedtoolsSerializer
)
from rest_framework import pagination



class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    def get_queryset(self):
        user = self.request.user  # Get the currently logged-in user
        return Cart.objects.filter(user=user)
  
class AddToCartViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','patch','delete']
    
    def get_queryset(self):
        user = self.request.user
        cart_id = user.cart.cart_id
        return CartItem.objects.filter(cart_id=cart_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return Update_cart_serializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        user = self.request.user
        cart_id = ""
        if user:
            try:
                cart_id = user.cart.cart_id
            except:
                print("not authenticated")
            return {'cart_id': cart_id}
        return{"error":"please login"}
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cart_id = instance.cart_id

        super().destroy(request, *args, **kwargs)

        remaining_items = CartItem.objects.filter(cart_id=cart_id)
        serializer = AddCartItemSerializer(remaining_items, many=True)  # Use AddToCartSerializer
        return Response(serializer.data)

##ORDER

class CheckoutView(APIView):
    def post(self, request):
        # Perform the payment process here
        # If the payment is successful, continue to the next step

        cart = request.user.cart
        order = cart.create_order()
        
        serializer = Order_Serializer(order)
        return Response(serializer.data)
    
    def get(self,request):
        user = request.user
        orders = Order.objects.filter(user = user)
        
        response_data = []
        for order in orders:
            
            order_serializer = Order_Serializer(orders)
            ordered_item = OrderedItem.objects.filter(order= order)
            orderd_items_serializer = OrderedtoolsSerializer(ordered_item , many = True)
            
            order_data = {
                "order":order_serializer.data,
                "tools":orderd_items_serializer.data
            }
            response_data.append(order_data)
        
        return Response(response_data)