from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Categories, Brand, Functionalities, Kits, Tools, ToolImages
from .serializers import CategorySerializer, BrandSerializer, FunctionalitySerializer, KitSerializer, ToolSerializer

# CATEGORY

class CategoryListView(APIView):
    def get(self, request):
        categories = Categories.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = CategorySerializer(category)
            tools = Tools.objects.filter(category = pk)
            tools_serializer= ToolSerializer(tools, many=True)
            response = {
                "category":serializer.data,
                "tools":tools_serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

  
#BRAND  
class BrandListView(APIView):
    def get(self, request):
        categories = Brand.objects.all()
        serializer = BrandSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailView(APIView):
    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = BrandSerializer(category)
            tools = Tools.objects.filter(brand = pk)
            tools_serializer= ToolSerializer(tools, many=True)
            response = {
                "category":serializer.data,
                "tools":tools_serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = BrandSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
#FUCTIONALITY  
class FunctionalityListView(APIView):
    def get(self, request):
        categories = Functionalities.objects.all()
        serializer = FunctionalitySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FunctionalitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FunctionalityDetailView(APIView):
    def get_object(self, pk):
        try:
            return Functionalities.objects.get(pk=pk)
        except Functionalities.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = FunctionalitySerializer(category)
            
            tools = Tools.objects.filter(functionalities = pk)
            tools_serializer= ToolSerializer(tools, many=True)
            response = {
                "category":serializer.data,
                "tools":tools_serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = FunctionalitySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
#KITS  
class KitsListView(APIView):
    def get(self, request):
        categories = Kits.objects.all()
        serializer = KitSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KitsDetailView(APIView):
    def get_object(self, pk):
        try:
            return Kits.objects.get(pk=pk)
        except Kits.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = KitSerializer(category)
            tools = Tools.objects.filter(kits = pk)
            tools_serializer= ToolSerializer(tools, many=True)
            response = {
                "category":serializer.data,
                "tools":tools_serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)           
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = KitSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
#TOOLS  
class ToolsListView(APIView):
    def get(self, request):
        categories = Tools.objects.all()
        serializer = ToolSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ToolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToolsDetailView(APIView):
    def get_object(self, pk):
        try:
            return Tools.objects.get(pk=pk)
        except Tools.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = ToolSerializer(category)
            tool_image = ToolImages.objects.filter(tool = pk)
            tools_image_serializer= ToolSerializer(tool_image, many=True)
            response = {
                "category":serializer.data,
                "tools":tools_image_serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category:
            serializer = ToolSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)