from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Trailer, TrailerDocument
from .serializers import TrailerSerializer, TrailerDocumentSerializer
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ExpiringTrailerDocs(request, id):
    today = datetime.today().date()
    ten_days = today + timedelta(days=10)
    docs = TrailerDocument.objects.filter(
        trailer_id=id,
        expiration_date__lte=ten_days,
        expiration_date__gte=today
    )
    titles = list(docs.values_list('category', flat=True))
    return Response({
        "expiring_trailer_documents": docs.count(),
        "titles": titles
    }, status=status.HTTP_200_OK)


def GetAllTrailers(request):
    userr = request.user
    trailers = Trailer.objects.filter(company=userr.company)
    serializer = TrailerSerializer(trailers, many=True)
    return Response({
        "number_of_trailer": trailers.count(),
        "trailers": serializer.data
    }, status=status.HTTP_200_OK)

def GetTrailer(request, id):
    userr = request.user
    trailer = Trailer.objects.filter(company=userr.company, id=id)
    serializer = TrailerSerializer(trailer, many=True)
    if not trailer.exists():
        return Response("No trailer found with that ID", status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)

def AddTrailer(request):
    userr = request.user
    data = request.data
    data['company'] = userr.company.code
    if userr.is_dispatcher:
        serializer = TrailerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

def UpdateTrailer(request, id):
    userr = request.user
    if userr.is_dispatcher:
        try:
            trailer = Trailer.objects.get(company=userr.company, id=id)
            serizalizer = TrailerSerializer(trailer, data=request.data, partial=True)
            if serizalizer.is_valid():
                serizalizer.save()
                return Response(serizalizer.data, status=status.HTTP_200_OK)
            return Response(serizalizer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trailer.DoesNotExist:
            return Response("Trailer not found", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

def DeleteTrailer(request, id):
    userr = request.user
    if userr.is_dispatcher:
        try:
            trailer = Trailer.objects.get(company=userr.company, id=id)
            trailer.delete()
            return Response("Trailer deleted", status=status.HTTP_200_OK)
        except Trailer.DoesNotExist:
            return Response("Trailer not found", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def TrailerViews(request, id=None):
    if request.method == 'GET':
        return GetTrailer(request, id)
    elif request.method == 'PATCH':
        return UpdateTrailer(request, id)
    elif request.method == 'DELETE':
        return DeleteTrailer(request, id)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def TrailerViewsNoID(request):
    if request.method == 'GET':
        return GetAllTrailers(request)
    elif request.method == 'POST':
        return AddTrailer(request)
    
""" Documents """

def DocumentUpload(request, trailer_id):
    try:
        trailer = Trailer.objects.get(id=trailer_id)
    except Trailer.DoesNotExist:
        return Response("Trailer not found", status=status.HTTP_404_NOT_FOUND)
    data = request.data.copy()
    data['trailer'] = trailer_id
    serializer = TrailerDocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetTrailerDocument(request, trailer_id, category):
    try:
        trailer = Trailer.objects.get(id=trailer_id)
    except Trailer.DoesNotExist: 
        return Response("Trailer not found", status=status.HTTP_404_NOT_FOUND)


    if category:
        documents = TrailerDocument.objects.filter(trailer=trailer_id, category=category)
    else:
        documents = TrailerDocument.objects.filter(trailer=trailer_id)
    
    serializer = TrailerDocumentSerializer(documents, many=True)
    return Response({
        "number_of_documents": documents.count(),
        "documents": serializer.data
    }, status=status.HTTP_200_OK)

def DeleteTrailerDocument(request, id):
    try:
        document = TrailerDocument.objects.get(id=id)
        document.delete()
        return Response("Document deleted", status=status.HTTP_200_OK)
    except TrailerDocument.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)    
    
def UpdateTrailerDocument(request, document_id):
    print(document_id)
    try:
        document = TrailerDocument.objects.get(id=document_id)

        serializer = TrailerDocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except TrailerDocument.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'PATCH', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def TrailerDocumentViews(request, id=None):
    if request.method == 'GET':
        return GetTrailerDocument(request._request, id, request.query_params.get("category"))
    elif request.method == 'POST':
        return DocumentUpload(request, id)
    elif request.method == 'PATCH':
        return UpdateTrailerDocument(request, id)
    elif request.method == 'DELETE':
        return DeleteTrailerDocument(request, id)
