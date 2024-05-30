from __future__ import unicode_literals
from .mpesa import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from order.views import CheckoutView 
from order.models import Cart 
from rest_framework import status
from .models import PaymentTransaction,Payment
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import paypalrestsdk 
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
 
 

paypalrestsdk.configure({
            "mode": "sandbox", # sandbox or live
            "client_id": "AXhrsP_no8GZjZu_vVXw64at5ItQUqH502y2ovLfINjagVtBGjJK4_mZQ_NRHVer38j5RUMjsLSay5pp",
            "client_secret": "ELiRbt7UjajjGTZGuXoYLTIZ4gx4TwEeqeAAxUilyOs-AbIRSBCGSwXl0GiV30sMp2lIGAbqkUkHAmJC"
})



# Initialize PayPal SDK


class CreatePaymentView(APIView):
    def post(self, request):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        total = sum([item.quantity * item.tool.price for item in cart.cart_items.all()])
        total = round(total, 2)  # Ensure the total is rounded to two decimal places

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
                        "name": "Cart Items",
                        "sku": "cart",
                        "price": "240",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "240",
                    "currency": "USD"
                },
                "description": "Payment for cart items."
            }]
        })

        if payment.create():
            # Save payment details to the database
            Payment.objects.create(
                user=user,
                payment_id=payment.id,
                amount=total,
                currency="USD",
                status="created"
            )
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

        payment = get_object_or_404(Payment, payment_id=payment_id)
        paypal_payment = paypalrestsdk.Payment.find(payment_id)

        if paypal_payment.execute({"payer_id": payer_id}):
            # Update payment status in the database
            payment.payer_id = payer_id
            payment.status = "executed"
            payment.save()
            return Response({"status": "Payment executed successfully"})
        else:
            return Response({"error": paypal_payment.error}, status=status.HTTP_400_BAD_REQUEST)

