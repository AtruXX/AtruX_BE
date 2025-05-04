from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Truck, TruckDocument
from .serializers import TruckSerializer, TruckDocumentSerializer

def GetAllTrucks(request):
    userr = request.user
    trucks = Truck.objects.filter(company=userr.company)
    serializer = TruckSerializer(trucks, many=True)
    return Response({
        "number_of_trucks": trucks.count(),
        "trucks": serializer.data
    }, status=status.HTTP_200_OK)

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

def UpdateTruck(request, id):
    userr = request.user
    if userr.is_dispatcher:
        try:
            truck = Truck.objects.get(company=userr.company, id=id)
            serizalizer = TruckSerializer(truck, data=request.data, partial=True)
            if serizalizer.is_valid():
                serizalizer.save()
                return Response(serizalizer.data, status=status.HTTP_200_OK)
            return Response(serizalizer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Truck.DoesNotExist:
            return Response("Truck not found", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

def DeleteTruck(request, id):
    userr = request.user
    if userr.is_dispatcher:
        try:
            truck = Truck.objects.get(company=userr.company, id=id)
            truck.delete()
            return Response("Truck deleted", status=status.HTTP_200_OK)
        except Truck.DoesNotExist:
            return Response("Truck not found", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def TruckViews(request, id=None):
    if request.method == 'GET':
        return GetTruck(request, id)
    elif request.method == 'PATCH':
        return UpdateTruck(request, id)
    elif request.method == 'DELETE':
        return DeleteTruck(request, id)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def TruckViewsNoID(request):
    if request.method == 'GET':
        return GetAllTrucks(request)
    elif request.method == 'POST':
        return AddTruck(request)
    
""" Documents """

def DocumentUpload(request, truck_id):
    try:
        truck = Truck.objects.get(id=truck_id)
    except Truck.DoesNotExist:
        return Response("Truck not found", status=status.HTTP_404_NOT_FOUND)
    data = request.data.copy()
    data['truck'] = truck_id
    serializer = TruckDocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetTruckDocument(request, truck_id, category):
    try:
        truck = Truck.objects.get(id=truck_id)
    except Truck.DoesNotExist: 
        return Response("Truck not found", status=status.HTTP_404_NOT_FOUND)
    
    if category:
        documents = TruckDocument.objects.filter(truck=truck_id, category=category)
    else:
        documents = TruckDocument.objects.filter(truck=truck_id)
    serializer = TruckDocumentSerializer(documents, many=True)
    return Response({
        "number_of_documents": documents.count(),
        "documents": serializer.data
    }, status=status.HTTP_200_OK)

def DeleteDocument(request, id):
    try:
        document = TruckDocument.objects.get(id=id)
        document.delete()
        return Response("Document deleted", status=status.HTTP_200_OK)
    except TruckDocument.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)    
    
def UpdateDocument(request, document_id):
    print(document_id)
    try:
        document = TruckDocument.objects.get(id=document_id)

        serializer = TruckDocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except TruckDocument.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'PATCH', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def DocumentViews(request, id=None):
    if request.method == 'GET':
        return GetTruckDocument(request._request, id, request.query_params.get("category"))
    elif request.method == 'POST':
        return DocumentUpload(request, id)
    elif request.method == 'PATCH':
        return UpdateDocument(request, id)
    elif request.method == 'DELETE':
        return DeleteDocument(request, id)
