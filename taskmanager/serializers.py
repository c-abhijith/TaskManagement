from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from taskmanager.models import Task



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = str(user.id)
        token['username'] = user.username
        token['role']=user.role
        return token

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_by','worked_hours', 'completion_report']

        
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['worked_hours', 'completion_report']

    def validate_worked_hours(self, value):
        if value is None:
            raise serializers.ValidationError("Worked hours is required.")
        if value < 0:
            raise serializers.ValidationError("Worked hours must be a non-negative number.")
        return value

    def validate_completion_report(self, value):
        if not value:
            raise serializers.ValidationError("Completion report is required.")
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Completion report cannot be empty.")
        return value

