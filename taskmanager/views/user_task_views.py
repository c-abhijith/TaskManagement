from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from taskmanager.models import Task
from taskmanager.serializers import TaskSerializer,TaskUpdateSerializer
from django.shortcuts import get_object_or_404

class UserTaskListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.role != "USER":
                return Response(
                    {"detail": "You do not have permission to view this."},
                    status=status.HTTP_403_FORBIDDEN
                )
            user = request.user  
            tasks = Task.objects.filter(assigned_to=user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": "Something went wrong.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class CompleteTaskAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            if request.user.role != "USER":
                return Response(
                    {"detail": "You do not have permission to view this."},
                    status=status.HTTP_403_FORBIDDEN
                )
            task = get_object_or_404(Task, id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": "Something went wrong.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, id):
        try:
            if request.user.role != "USER":
                return Response(
                    {"detail": "You do not have permission to view this."},
                    status=status.HTTP_403_FORBIDDEN
                )
            task = get_object_or_404(Task, id=id)
            serializer = TaskUpdateSerializer(task, data=request.data)
            if serializer.is_valid():
                task.status = "Completed"
                serializer.save()
                return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "Something went wrong.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def patch(self, request, id):
        try:
            if request.user.role != "USER":
                return Response(
                    {"detail": "You do not have permission to view this."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            task = get_object_or_404(Task, id=id)
            task.status = "InProgress"
            task.save()
            
            print(task.status)
            return Response(
                {"message": "Task updated successfully."},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"detail": "Something went wrong.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
