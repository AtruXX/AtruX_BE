from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.models import User, Driver, Document
from rest_framework.response import Response
from .serializers import UserSerializer, DocumentSerializer
from rest_framework import status

""" PAGES """

def activation_page(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'pages/verify_email.html', context)

def reset_password_page(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'pages/change_password.html', context)

def activation_page_ok(request):
    return render(request, "pages/verify_email_success.html");

def reset_pass_ok(request):
    return render(request, "pages/change_password_success.html")

""" API VIEWS """

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllDrivers(request):
    userr = request.user
    if userr.is_dispatcher:
        drivers = User.objects.filter(company=userr.company, is_driver=True)
        serializer = UserSerializer(drivers, many=True)
        return Response({
            "number_of_drivers": drivers.count(),
            "drivers": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDriver(request, id):
    userr = request.user
    if userr.is_dispatcher:
        driver = User.objects.filter(company=userr.company, is_driver=True, id=id)
        serializer = UserSerializer(driver, many=True)
        if not driver.exists():
            return Response("No driver found with that ID", status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def GiveRating(request, id):
    user = request.user
    if user.is_dispatcher:
        driver_user = User.objects.get(id=id)
        driver = Driver.objects.get(user=driver_user)
        rating = request.data.get('rating')
        if rating is not None and rating >= 1 and rating <= 5:
            driver.rating += rating
            driver.nr_of_ratings += 1
            driver.save()
            serializer = UserSerializer(driver_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Invalid rating", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ChangeStatus(request):
    user = request.user
    if user.is_driver:
        driver = Driver.objects.get(user=user)
        driver.on_road = not driver.on_road
        driver.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("You are not a driver", status=status.HTTP_403_FORBIDDEN)

def DocumentUpload(request):
    userr = request.user
    data = request.data.copy()
    data['user'] = userr.id
    serializer = DocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetUserDocuments(request, category):
    userr = request.user
    if category:
        documents = Document.objects.filter(user=userr, category=category)
    else:
        documents = Document.objects.filter(user=userr)
    
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def DeleteUserDocument(request, id):
    userr = request.user
    try:
        document = Document.objects.get(id=id)
        if document.user != userr:
            return Response("You are not the owner of this document", status=status.HTTP_403_FORBIDDEN)
        document.delete()
        return Response("Document deleted", status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)    

def UpdateDocument(request, id):
    userr = request.user
    try:
        document = Document.objects.get(id=id)

        if document.user != userr:
            return Response("You are not the owner of this document", status=status.HTTP_403_FORBIDDEN)
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Document.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'GET', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def DocumentViews(request, id=None):
    if request.method == 'POST':
        return DocumentUpload(request)
    elif request.method == 'GET':
        return GetUserDocuments(request._request, request.query_params.get("category"))
    elif request.method == 'DELETE':
        return DeleteUserDocument(request, id)
    elif request.method == 'PATCH':
        return UpdateDocument(request, id)
    
    