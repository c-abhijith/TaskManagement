# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


# DRF API view
class HelloAPIView(APIView):
    def get(self, request):
        data = {"message": "Hello from DRF!"}
        return Response(data, status=status.HTTP_200_OK)

# Django template view
def show_hello(request):
    
    data = {"message": "Hello from DRF!"}
    return render(request, 'hello.html', {'data': data})
