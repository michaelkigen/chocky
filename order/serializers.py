from rest_framework import serializers
from .models import CartItem, Order, Cart, OrderedItem
from tools.serializers import ToolSerializer
from tools.models import Tools

class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField(method_name='calculate_subtotal')  # Add SerializerMethodField for subtotal

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'tool', 'quantity', 'subtotal']  # Update fields to include subtotal

    def calculate_subtotal(self, obj):
        return obj.quantity * obj.tool.price  # Calculate subtotal based on quantity and tool price

    

class AddCartItemSerializer(serializers.ModelSerializer):
    tool = serializers.UUIDField()  # Change id to tool and use UUIDField for tool

    def validate_tool(self, value):
        if not Tools.objects.filter(pk=value).exists():
            raise serializers.ValidationError('There is no such product')
        return value
        
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        tool_id = self.validated_data['tool']  # Change id to tool
        quantity = self.validated_data['quantity']
        
        try:
            item = CartItem.objects.get(tool_id=tool_id, cart_id=cart_id)  
            item.quantity += quantity
            item.save()
            self.instance = item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(tool_id=tool_id, cart_id=cart_id, quantity=quantity)  
            
    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'tool', 'quantity'] 


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)  # Change 'cartItems' to 'cart_items'

    total = serializers.SerializerMethodField(method_name='calculate_total_price')
    cart_id = serializers.UUIDField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'created_at', 'cart_items', 'total']
        extra_kwargs = {'created_at': {'read_only': True}}

    def calculate_total_price(self, cart):
        items = cart.cart_items.all() 
        print("items ",items)# Update to use 'cart_items'
        price = sum([item.quantity * item.tool.price for item in items])
        print(price)
        return price
    
class Update_cart_serializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'quantity']
        extra_kwargs = {'cart_item_id':{'read_only': True}}
        
        
        
class OrderedtoolsSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField(method_name= 'total')

    class Meta:
        model = OrderedItem
        fields = ['tool', 'quantity', 'sub_total']

    def total(self, obj):
        return obj.quantity * obj.tool.price
    
class Order_Serializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(method_name='total_price')

    class Meta:
        model = Order
        fields = ['order_id', 'receipt', 'state', 'created_at', 'total', 'payment_mode', 'user']
        extra_kwargs = {'user': {'read_only': True}}

    def total_price(self, order):
        items = order.ordered_items.all()  # Access related items correctly
        price = sum([item.quantity * item.tool.price for item in items])
        return price


class OrderIdSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    
