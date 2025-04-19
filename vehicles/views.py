from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Truck
from .serializers import TruckSerializer

def GetAllTrucks(request):
    userr = request.user
    trucks = Truck.objects.filter(company=userr.company)
    serializer = TruckSerializer(trucks, many=True)
    return Response({
        "number_of_trucks": trucks.count(),
        "trucks": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetTruck(request, id):
    userr = request.user
    truck = Truck.objects.filter(company=userr.company, id=id)
    serializer = TruckSerializer(truck, many=True)
    if not truck.exists():
        return Response("No truck found with that ID", status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)

def AddTruck(request):
    userr = request.user
    data = request.data
    data['company'] = userr.company.code
    if userr.is_dispatcher:
        serializer = TruckSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def TruckViews(request):
    if request.method == 'GET':
        return GetAllTrucks(request)
    if request.method == 'POST':
        return AddTruck(request)
