from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .mpesa import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from order.views import CheckoutView , CartViewSet
from order.models import Cart , CartItem ,Order
from django.db.models import Sum
from authentication.models import User
from rest_framework import generics, permissions,status
from .models import PaymentTransaction
from django.shortcuts import get_object_or_404
from django.conf import settings
# Create your views here.
        


class SubmitView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        phone_number = data.get('phone_number')
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        if cart is None:
            return Response({"detail": "Cart not found."}, status=HTTP_404_NOT_FOUND)

        total = sum([item.quantity * item.tool.price for item in cart.cart_items.all()])
        amount = total
        print('the total amount is: ', amount)

        entity_id = 0
        if data.get('entity_id'):
            entity_id = data.get('entity_id')

        paybill_account_number = None
        if data.get('paybill_account_number'):
            paybill_account_number = data.get('paybill_account_number')

        trans = PaymentTransaction.objects.create()
        print('TRANSACTION INSTANCE :', trans)
        transaction_id = sendSTK(phone_number, amount, entity_id, transaction_id=trans)

        # b2c()
        
        
        message = {"status": "ok", "transaction_id": transaction_id}
        return Response(message, status=HTTP_200_OK)


class CheckTransactionOnline(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        trans_id = request.data['transaction_id']
        transaction = PaymentTransaction.objects.filter(trans_id=trans_id).first()

        try:
            if transaction and transaction.checkout_request_id:
                status_response = check_payment_status(transaction.checkout_request_id)
                status = status_response.get('status')
                print('STATUS: ', status)
                message = status_response.get('message')
                
                if status:
                    user = request.user
                    checkout_view = CheckoutView()
                    order_id = checkout_view.post(request).data.get('order_id')
                    print('ORDER_ID :', order_id)

                    transaction.order_id = order_id
                    transaction.is_finished = True
                    transaction.is_successful = True
                    transaction.user = user
                    transaction.message = message
                    transaction.save()
                    print('SAVED TRANSACTION :', transaction)
                    
             
                return JsonResponse(status_response, status=200)
            else:
                return JsonResponse({
                    "message": "Server Error. Transaction not found",
                    "status": False
                }, status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            }, status=400)



class CheckTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        trans_id = data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.is_finished,
                    "successful": transaction.is_successful
                },
                    status=200)
            else:
                # TODO : Edit order if no transaction is found
                return JsonResponse({
                    "message": "Error. Transaction not found",
                    "status": False
                },
                    status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class RetryTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction and transaction.is_successful:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.is_finished,
                    "successful": transaction.is_successful
                },
                    status=200)
            else:
                response = sendSTK(
                    phone_number=transaction.phone_number,
                    amount=transaction.amount,
                    orderId=transaction.order_id,
                    transaction_id=trans_id)
                return JsonResponse({
                    "message": "ok",
                    "transaction_id": response
                },
                    status=200)

        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Error. Transaction not found",
                "status": False
            },
                status=400)


class ConfirmView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
       # request_data = json.dumps(request.data)
        request_data = request.data
        print("the data  is: " , request_data)
        body = request_data
        print("the body is: ",body)
        
        resultcode = body.get('stkCallback').get('ResultCode')
        # Perform your processing here e.g. print it out...
        if resultcode == 0:
            print('Payment successful')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
            for data in metadata:
                if data.get('Name') == "MpesaReceiptNumber":
                    receipt_number = data.get('Value')
            transaction = PaymentTransaction.objects.get(
                checkout_request_id=requestId)
            if transaction:
                transaction.receipt_number = receipt_number
                transaction.is_finished = True
                transaction.is_successful = True
                transaction.save()

        else:
            print('unsuccessfull')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            transaction = PaymentTransaction.objects.get(
                checkout_request_id=requestId)
            if transaction:
                transaction.is_finished = True
                transaction.is_successful = False
                transaction.save()

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1237867865"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)

    def get(self, request):
        return Response("Confirm callback", status=HTTP_200_OK)


class ValidateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
        request_data = request.data

        # Perform your processing here e.g. print it out...
        print("validate data" + request_data)

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1234567890"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)
    
    
# class PaymentTransactionListView(generics.ListAPIView):
#     serializer_class = PaymentTransactionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return PaymentTransaction.objects.all()

# class SearchTransaction(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, trans_id, format=None): 
#         # Use a GET request and specify trans_id as a URL parameter
#         # This allows you to retrieve a specific transaction directly
#         transaction = get_object_or_404(PaymentTransaction, trans_id=trans_id)

#         # Now, you can serialize the transaction and return it as a response
#         serializer = PaymentTransactionSerializer(transaction)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        

# class SortTransactionByAccount(View):
#     def get(self, request, phone_number):
#         # Retrieve the user object with the given phone number
#         user = get_object_or_404(User, phone_number=phone_number)
        
#         # Retrieve all payment transactions made by the user
#         transactions = PaymentTransaction.objects.filter(user=user)
        
#         # Prepare the data to return
#         transaction_data = []
#         for transaction in transactions:
#             transaction_data.append({
#                 'trans_id': transaction.trans_id,
#                 'amount': str(transaction.amount),
#                 'is_finished': transaction.is_finished,
#                 'is_successful': transaction.is_successful,
#                 'order_id': str(transaction.order_id),
#                 'checkout_request_id': transaction.checkout_request_id,
#                 'date_created': transaction.date_created.strftime('%Y-%m-%d %H:%M:%S'),
#                 'receipt_number': transaction.receipt_number,
#                 'message': transaction.message
#             })
        
#         return JsonResponse({'transactions': transaction_data})
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from paypalrestsdk import Payment , configure

# class PaymentView(APIView):
#     def post(self, request):
#         # Create a payment object
#         configure({
#             "mode": "sandbox", # sandbox or live
#             "client_id": "AXhrsP_no8GZjZu_vVXw64at5ItQUqH502y2ovLfINjagVtBGjJK4_mZQ_NRHVer38j5RUMjsLSay5pp",
#             "client_secret": "ELiRbt7UjajjGTZGuXoYLTIZ4gx4TwEeqeAAxUilyOs-AbIRSBCGSwXl0GiV30sMp2lIGAbqkUkHAmJC" })
#         payment = Payment({
#             'intent': 'sale',
#             'payer': {
#                 'payment_method': 'paypal'
#             },
#             'redirect_urls': {
#                 'return_url': 'http://127.0.0.1:8000/',
#                 'cancel_url': 'http://127.0.0.1:8000/'
#             },
#             'transactions': [{
#                 'item_list': {
#                     'items': [{
#                         'name': 'item',
#                         'sku': 'item-sku',
#                         'price': '10.00',
#                         'currency': 'USD',
#                         'quantity': 1
#                     }]
#                 },
#                 'amount': {
#                     'currency': 'USD',
#                     'total': '10.00'
#                 }
#             }]
#         })

#         # Redirect the user to PayPal to authorize the payment
#         return Response({'redirect_url':'d'})
    
# class PaymentResponseView(APIView):
#     def post(self, request):
#         # Get the payment ID from the request
#         payment_id = request.data['payment_id']

#         # Get the payment object from PayPal
#         payment = Payment.find(payment_id)

#         # Verify the payment
#         if payment.state == 'approved':
#             # Update the order status
#             # ...
#             return Response({'message': 'Payment successful'})
#         else:
#             # Handle payment failure
#             # ...
#             return Response({'message': 'Payment failed'})
        
        
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
            "mode": "sandbox", # sandbox or live
            "client_id": "AXhrsP_no8GZjZu_vVXw64at5ItQUqH502y2ovLfINjagVtBGjJK4_mZQ_NRHVer38j5RUMjsLSay5pp",
            "client_secret": "ELiRbt7UjajjGTZGuXoYLTIZ4gx4TwEeqeAAxUilyOs-AbIRSBCGSwXl0GiV30sMp2lIGAbqkUkHAmJC"
})

class CreatePaymentView(APIView):
    def post(self, request):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "https://chocky-0b334251234b.herokuapp.com/",
                "cancel_url": "https://chocky-0b334251234b.herokuapp.com/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "1.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "1.00",
                    "currency": "USD"
                },
                "description": "This is the payment transaction description."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return Response({"approval_url": approval_url})
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

class ExecutePaymentView(APIView):
    def post(self, request):
        payment_id = request.data.get('paymentID')
        payer_id = request.data.get('payerID')
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            return Response({"status": "Payment executed successfully"})
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)
