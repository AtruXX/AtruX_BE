from rest_framework import serializers
from .models import Transport, TransportDocument, Route, Point, CMR

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
        fields = ['name', 'latitude', 'longitude']

class RouteSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Route
        fields = '__all__'

    def create(self, validated_data):
        points_data = validated_data.pop('points')
        route = Route.objects.create(**validated_data)
        for point_data in points_data:
            Point.objects.create(route=route, **point_data)
        return route
        
class CMRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMR
        fields = '__all__'
        