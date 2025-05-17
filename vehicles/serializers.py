from rest_framework import serializers
from .models import Truck, TruckDocument, Trailer, TrailerDocument

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

class TruckDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckDocument
        fields = '__all__'

    def validate(self, data):
            if not self.partial:
                required_fields = ['document', 'category', 'title']

                for field in required_fields:
                    if field not in data:
                        raise serializers.ValidationError(f"{field} is required.")
            return data
    
class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = '__all__'

class TrailerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailerDocument
        fields = '__all__'

    def validate(self, data):
            if not self.partial:
                required_fields = ['document', 'category', 'title']

                for field in required_fields:
                    if field not in data:
                        raise serializers.ValidationError(f"{field} is required.")
            return data
    