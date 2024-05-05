from django.contrib import admin
from django.urls import path
from .views import( SubmitView, CheckTransaction, ConfirmView, CheckTransactionOnline,PaymentView,PaymentResponseView )

urlpatterns = [
    path('send/', SubmitView.as_view(), name='submit'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('check-online/', CheckTransactionOnline.as_view(), name='confirm-online'),
    path('check-transaction/', CheckTransaction.as_view(), name='check_transaction'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment-response/', PaymentResponseView.as_view(), name='payment-response')

]