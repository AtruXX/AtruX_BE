from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import User, Dispatcher, Driver, Document
from utils.utils_enums import PERSONAL_DOCUMENTS_CATEGORIES


User = get_user_model()

class UserCreateSerializerr(UserCreateSerializer):
    company = serializers.CharField(required=False, allow_null=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "company", "password", "is_dispatcher", "is_driver", "phone_number")

class DriverSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['average_rating', 'on_road']

    def get_average_rating(self, obj):
        if obj.nr_of_ratings == 0:
            return 0.0
        return round(obj.rating / obj.nr_of_ratings, 2)

class DispatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatcher
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    dispatcher = DispatcherSerializer()
    company = serializers.SerializerMethodField(source='company')
    license_expiration_date = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        exclude = ["password"]

    def get_company(self, obj):
        return obj.company.name

    def assign_serializer(self, obj):
        if obj.is_driver:
            driver = Driver.objects.get(user=obj)
            return DriverSerializer(driver).data
        elif obj.is_dispatcher:
            dispatcher = Dispatcher.objects.get(user=obj)
            return DispatcherSerializer(dispatcher).data
        return None
    
    def get_license_expiration_date(self, obj):
        try:
            license = Document.objects.get(user=obj.id, category="permis_de_conducere")
        except Document.DoesNotExist:
            return None
        if license.expiration_date:
            return license.expiration_date
        return None
    
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate_category(self, value):
        if value not in PERSONAL_DOCUMENTS_CATEGORIES:
            raise serializers.ValidationError("Invalid category.")
        return value

    def validate(self, data):
            if not self.partial:
                required_fields = ['document', 'category', 'title']

                for field in required_fields:
                    if field not in data:
                        raise serializers.ValidationError(f"{field} is required.")
            return data