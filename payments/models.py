# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.contrib.auth.models import User


class PaymentTransaction(models.Model):
    trans_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_finished = models.BooleanField(default=False)
    is_successful = models.BooleanField(default=False)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    checkout_request_id = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    receipt_number = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.PROTECT,related_name='transactions', null= True )
    message = models.CharField(max_length=200, null= True)
    
    
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{} {} {}".format(self.phone_number, self.amount, self.checkout_request_id)

#pypal

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=255, unique=True)
    payer_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment {self.payment_id} - {self.user.username}'