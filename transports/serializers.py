from rest_framework import serializers
from .models import Transport, TransportDocument

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


