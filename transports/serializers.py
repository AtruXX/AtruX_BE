from rest_framework import serializers
from .models import Transport, TransportDocument, Route, Point

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'

class TransportDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDocument
        fields = '__all__'

    def validate(self, data):
            if not self.partial:
                required_fields = ['document', 'category', 'title']

                for field in required_fields:
                    if field not in data:
                        raise serializers.ValidationError(f"{field} is required.")
            return data
    
class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Route
        fields = '__all__'
        