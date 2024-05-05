from django.db import models
from tools.models import Tools
import uuid
from authentication.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart ID: {self.cart_id}, User: {self.user.username}"

    @receiver(post_save, sender=User)
    def create_user_cart(sender, instance, created, **kwargs):
        if created:
            Cart.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_cart(sender, instance, **kwargs):
        instance.cart.save()

        
    def create_order(self):
       
        order = Order.objects.create(user=self.user , state='p' )

        cart_items = self.cart_items.all()

        for cart_item in cart_items:
            OrderedItem.objects.create(
                tool=cart_item.tool,
                order=order,
                quantity=cart_item.quantity
            )

        self.cart_items.all().delete()  # Empty the cart after creating the order

        return order


class CartItem(models.Model):
    cart_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items") # Update related_name
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE, related_name='tool_items')  # Update related_name
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Cart Item ID: {self.cart_item_id}, Tool: {self.tool.name}, Quantity: {self.quantity}"



MODE_OF_PAYMENTS = (
    ('MPESA','mpesa'),
    ('QCOINS','qcoins')
)


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    CANCELED = 'X'
    STATUSES = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (CANCELED, 'Canceled'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=1, choices=STATUSES, default=PENDING)
    receipt = models.FileField(upload_to='receipts', null=True)
    payment_mode = models.CharField(max_length=50, choices=MODE_OF_PAYMENTS, default='MPESA')

    def __str__(self):
        return f"Order ID: {self.order_id}, User: {self.user}, Status: {self.get_state_display()}"

class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE, related_name='ordered_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Ordered Item: {self.tool.name}, Quantity: {self.quantity}"

