from rest_framework import serializers
from myapp.models import Student, Userdata

class UserdataSerializer(serializers.ModelSerializer):

    #username=serializers.CharField(max_length=20)
    #password=serializers.CharField(max_length=20)
    #mobno = serializers.IntegerField()

    class Meta:
        model=Userdata
        #exclude=['password']
        fields='__all__'

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Student
        fields='__all__'