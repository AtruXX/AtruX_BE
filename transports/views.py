from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Transport, Route, Point, CMR
from .models import TransportDocument
from .serializers import TransportSerializer, TransportDocumentSerializer, RouteSerializer, PointSerializer, CMRSerializer

def IsUserAssignedToTransport(user, transport):
    if user.is_dispatcher:
        return transport.dispatcher == user
    else:
        return transport.driver == user

def GetAllTransports(request):
    user = request.user
    driver_id = request.query_params.get("driver")

    if user.is_dispatcher:
        if driver_id:
            transports = Transport.objects.filter(company=user.company, driver=driver_id)
        else:
            transports = Transport.objects.filter(company=user.company)
    else:
        transports = Transport.objects.filter(company=user.company, driver=user)
    serializer = TransportSerializer(transports, many=True)
    return Response({
        "number_of_transports": transports.count(),
        "transports": serializer.data
    }, status=status.HTTP_200_OK)

def GetTransport(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    serializer = TransportSerializer(transport)
    return Response(serializer.data, status=status.HTTP_200_OK)

def CreateTransport(request):
    userr = request.user
    data = request.data
    data['company'] = userr.company.code
    data['dispatcher'] = userr.id
    if userr.is_dispatcher:
        serializer = TransportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def TransportViewsNoID(request):
    if request.method == 'GET':
        return GetAllTransports(request)
    if request.method == 'POST':
        return CreateTransport(request)
    

def UpdateTransport(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(id=id)

        if not IsUserAssignedToTransport(userr, transport):
            return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
        
        serializer = TransportSerializer(transport, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)

def DeleteTransport(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    if not IsUserAssignedToTransport(userr, transport):
        return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
    
    transport.delete()
    return Response("Transport deleted", status=status.HTTP_200_OK)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def TransportViews(request, id=None):
    if request.method == 'PATCH':
        return UpdateTransport(request, id)
    if request.method == 'DELETE':
        return DeleteTransport(request, id)
    if request.method == 'GET':
        return GetTransport(request, id)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ActiveTransports(request):
    user = request.user
    transports = Transport.objects.filter(company=user.company, is_finished=False)

    serializer = TransportSerializer(transports, many=True)
    return Response({
        "number_of_active_transports": transports.count(),
        "active_transports": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def InactiveTransports(request):
    user = request.user
    transports = Transport.objects.filter(company=user.company, is_finished=True)

    serializer = TransportSerializer(transports, many=True)
    return Response({
        "number_of_inactive_transports": transports.count(),
        "inactive_transports": serializer.data
    }, status=status.HTTP_200_OK)


def UploadTransportDocuments(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    if not IsUserAssignedToTransport(userr, transport):
        return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
        
    data = request.data.copy()
    data['transport'] = id
    serializer = TransportDocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetTransportDocuments(request, id, category):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    if not IsUserAssignedToTransport(userr, transport):
        return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)

    if category:
        documents = TransportDocument.objects.filter(transport=transport, category=category)
    else:
        documents = TransportDocument.objects.filter(transport=transport)

    serializer = TransportDocumentSerializer(documents, many=True)
    return Response({
        "number_of_documents": documents.count(),
        "documents": serializer.data
    }, status=status.HTTP_200_OK)

def UpdateTransportDocument(request, id):
    userr = request.user
    try:
        document = TransportDocument.objects.get(id=id)
    except TransportDocument.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)
    
    transport = document.transport
    if not IsUserAssignedToTransport(userr, transport):
        return Response("You are not assigned to the transport related to this document", status=status.HTTP_403_FORBIDDEN)

    serializer = TransportDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def DeleteTransportDocument(request, id):
    userr = request.user
    try:
        document = TransportDocument.objects.get(id=id)
    except TransportDocument.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)
    
    transport = document.transport
    if not IsUserAssignedToTransport(userr, transport):
        return Response("You are not assigned to the transport related to this document", status=status.HTTP_403_FORBIDDEN)
    
    document.delete()
    return Response("Document deleted", status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def TransportDocumentViews(request, id=None):
    if request.method == 'GET':
        return GetTransportDocuments(request, id, request.query_params.get("category"))
    if request.method == 'POST':
        return UploadTransportDocuments(request, id)
    if request.method == 'PATCH':
        return UpdateTransportDocument(request, id)
    if request.method == 'DELETE':
        return DeleteTransportDocument(request, id)


def GetRoute(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    route = Route.objects.filter(transport=transport)
    if not route.exists():
        return Response("Route not found", status=status.HTTP_404_NOT_FOUND)
    
    serializer = RouteSerializer(route, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
def CreateRoute(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
    except Transport.DoesNotExist:
        return Response({"error": "Transport not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['transport'] = transport.id
    data['date'] = date.today()

    print(data)

    serializer = RouteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def RouteViews(request, id=None):
    if request.method == 'GET':
        return GetRoute(request, id)
    if request.method == 'POST':
        return CreateRoute(request, id)
    


def CreateCMR(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
        if not IsUserAssignedToTransport(userr, transport):
            return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['transport'] = transport.id
    data['driver'] = transport.driver.id
    data['dispatcher'] = transport.dispatcher.id

    serializer = CMRSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetCMR(request, id):
    userr = request.user
    try:
        transport = Transport.objects.get(company=userr.company, id=id)
        if not IsUserAssignedToTransport(userr, transport):
            return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)
    
    cmr = CMR.objects.filter(transport=transport)
    if not cmr.exists():
        return Response("CMR not found", status=status.HTTP_404_NOT_FOUND)
    
    serializer = CMRSerializer(cmr, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def UpdateCMR(request, id):
    userr = request.user
    try:
        cmr = CMR.objects.get(id=id)
        transport = cmr.transport
        if not IsUserAssignedToTransport(userr, transport):
            return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
    except CMR.DoesNotExist:
        return Response("CMR not found", status=status.HTTP_404_NOT_FOUND)
    
    serializer = CMRSerializer(cmr, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def DeleteCMR(request, id):
    userr = request.user
    try:
        cmr = CMR.objects.get(id=id)
        transport = cmr.transport
        if not IsUserAssignedToTransport(userr, transport):
            return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
    except CMR.DoesNotExist:
        return Response("CMR not found", status=status.HTTP_404_NOT_FOUND)
    
    cmr.delete()
    return Response("CMR deleted", status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def CMRViews(request, id=None):
    if request.method == 'POST':
        return CreateCMR(request, id)
    if request.method == 'GET':
        return GetCMR(request, id)
    if request.method == 'PATCH':
        return UpdateCMR(request, id)
    if request.method == 'DELETE':
        return DeleteTransport(request, id)