from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Orderd_course
from rest_framework.permissions import IsAuthenticated
from .serializers import Orderd_couse_serializer
from payments.mpesa import sendSTK
from payments.models import PaymentTransaction
from courses.models import Course

class Orders_course_view(APIView):
    def get(self, request):
        user = request.user
        courses = Orderd_course.objects.filter(user=user)
        if not courses:
            return Response({"error":"courses not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = Orderd_couse_serializer(courses , many = True)
        return Response(serializer.data , status= status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user

        serializer = Orderd_couse_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            phone = validated_data['phone']
            cos_id = validated_data['courses']
          
            amount = cos_id.price

            trans = PaymentTransaction.objects.create()
            entity_id = 0
            print('TRANSACTION INSTANCE:', trans)
            transaction_id = sendSTK(phone, amount, entity_id, transaction_id=trans)
            
            # Assign user before saving
            serializer.save(user=user)
            
            message = {"data": serializer.data, "status": "ok", "transaction_id": transaction_id}
            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class All_Orderd_courses(APIView):
    def get(slef):
        courses = Orderd_course.objects.all()
        serializer = Orderd_couse_serializer(courses, many=True)
        return Response(serializer.data)