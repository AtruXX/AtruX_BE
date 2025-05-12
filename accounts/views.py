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

def DocumentExists(request, userr):
    category = request.data.get('category')
    if category == 'permis_de_conducere' or category == request.data.get('buletin'):
        documents = Document.objects.filter(user=userr, category=category)
        if documents.exists():
            return True
    return False

def DocumentUpload(request):
    userr = request.user
    if DocumentExists(request, userr):
        return Response("You already have a document of this type", status=status.HTTP_400_BAD_REQUEST)
    
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
    if DocumentExists(request, userr) and request.data.get('category') != None:
        return Response("You already have a document of this type", status=status.HTTP_400_BAD_REQUEST)
    
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


def validate_driver(driver_id):
        try:
            driver = User.objects.get(id=driver_id)
            if not driver:
                return Response("No driver found with that ID", status=status.HTTP_404_NOT_FOUND)
            if not driver.is_driver:
                return Response("This user is not a driver", status=status.HTTP_400_BAD_REQUEST)
            return driver
        except User.DoesNotExist:
            return Response("No user found with that ID", status=status.HTTP_404_NOT_FOUND)


def GetDriverDocuments(request, driver_id):
    userr = request.user
    if not userr.is_dispatcher:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)
    
    driver = validate_driver(driver_id)
    if isinstance(driver, Response):
        return driver
    
    documents = Document.objects.filter(user=driver)
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def DriverDocumentUpload(request, driver_id):
    userr = request.user
    if not userr.is_dispatcher:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)
    
    driver = validate_driver(driver_id)
    if isinstance(driver, Response):
        return driver

    if DocumentExists(request, driver):
        return Response("The driver already has a document of this type", status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data['user'] = driver.id
    serializer = DocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def DeleteDriverDocument(request, driver_id, document_id):
    userr = request.user
    if not userr.is_dispatcher:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)
    
    driver = validate_driver(driver_id)
    if isinstance(driver, Response):
        return driver

    try:
        document = Document.objects.get(id=document_id)
        document.delete()
        return Response("Document deleted", status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)


def UpdateDriverDocument(request, driver_id, document_id):
    userr = request.user
    if not userr.is_dispatcher:
        return Response("You are not a dispatcher", status=status.HTTP_403_FORBIDDEN)
    
    if DocumentExists(request, userr) and request.data.get('category') != None:
        return Response("You already have a document of this type", status=status.HTTP_400_BAD_REQUEST)
    
    validation_response = validate_driver(driver_id)
    if isinstance(validation_response, Response):
        return validation_response

    try:
        document = Document.objects.get(id=document_id)
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Document.DoesNotExist:
        return Response("Document not found", status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def DriverDocumentViews(request, driver_id=None, document_id=None):
    if request.method == 'GET':
        return GetDriverDocuments(request, driver_id)
    if request.method == 'POST':
        return DriverDocumentUpload(request, driver_id)
    if request.method == 'DELETE':
        return DeleteDriverDocument(request, driver_id, document_id)
    if request.method == 'PATCH':
        return UpdateDriverDocument(request, driver_id, document_id)
    
    