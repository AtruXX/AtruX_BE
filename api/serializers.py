from rest_framework import serializers
from base.models import dispacher

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = dispacher
        fields = '__all__'