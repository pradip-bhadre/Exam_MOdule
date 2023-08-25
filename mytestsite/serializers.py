from rest_framework import serializers

from myapp.models import Userdata

class UserdataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Userdata
        fields=["username","password","mobno"]