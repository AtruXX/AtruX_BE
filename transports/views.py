from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Transport
from .models import TransportDocument
from .serializers import TransportSerializer

def GetAllTransports(request):
    user = request.user
    if user.is_dispatcher:
        transports = Transport.objects.filter(company=user.company)
    else:
        transports = Transport.objects.filter(company=user.company, driver=user)
    serializer = TransportSerializer(transports, many=True)
    return Response({
        "number_of_transports": transports.count(),
        "transports": serializer.data
    }, status=status.HTTP_200_OK)

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
        transport = Transport.objects.get(company=userr.company, id=id)
        if userr.is_dispatcher:
            if transport.dispatcher != userr:
                return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
        else:
            if transport.driver != userr:
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
        if userr.is_dispatcher:
            if transport.dispatcher != userr:
                return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
        else:
            if transport.driver != userr:
                return Response("You are not assigned to this transport", status=status.HTTP_403_FORBIDDEN)
        transport.delete()
        return Response("Transport deleted", status=status.HTTP_200_OK)
    except Transport.DoesNotExist:
        return Response("Transport not found", status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def TransportViews(request, id=None):
    if request.method == 'PATCH':
        return UpdateTransport(request, id)
    if request.method == 'DELETE':
        return DeleteTransport(request, id)


