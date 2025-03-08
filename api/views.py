from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.serializers import UserCreateSerializerr
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.models import User, Driver, Dispatcher, Document
from base.models import Point, Route, Transport
from datetime import date

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDrivers(request):
    userr = request.user
    if userr.is_dispatcher:
        driver_users = User.objects.filter(company=userr.company, is_driver=True)
        driver_list = []
        for driver in driver_users:
            driver_prorierties = Driver.objects.get(user=driver)
            if driver_prorierties.nr_of_ratings == 0:
                rating = 0.0
            else:
                rating = driver_prorierties.rating / driver_prorierties.nr_of_ratings
            driver_json = {
                'id': driver.id,
                'email': driver.email,
                'name': driver.name,
                'company': driver.company.name,
                'is_dispatcher': driver.is_dispatcher,
                'is_driver': driver.is_driver,
                'rating': rating,
                'on_road': driver_prorierties.on_road,
            }
            driver_list.append(driver_json)
        return Response(driver_list)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfile(request):
    userr = request.user
    if userr.is_driver:
        driver = Driver.objects.get(user=userr)
        if driver.nr_of_ratings == 0:
                rating = 0.0
        else:
            rating = driver.rating / driver.nr_of_ratings
        profile_json = {
            'id': userr.id,
            'email': userr.email,
            'name': userr.name,
            'company': userr.company.name,
            'is_dispatcher': userr.is_dispatcher,
            'is_driver': userr.is_driver,
            'rating': rating,
            'on_road': driver.on_road
        }
    else:
        profile_json = {
            'id': userr.id,
            'email': userr.email,
            'name': userr.name,
            'company': userr.company.name,
            'is_dispatcher': userr.is_dispatcher,
            'is_driver': userr.is_driver
        }
    return Response(profile_json, status=200)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GiveRating(request):
    userr = request.user
    if userr.is_dispatcher:
        driver_id = request.data.get('driver_id')
        rating = request.data.get('rating')
        driver = User.objects.get(id=driver_id)
        driver_driver = Driver.objects.get(user=driver)
        driver_driver.rating += rating
        driver_driver.nr_of_ratings += 1
        driver_driver.save()
        return Response("Rating given", status=200)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ChangeStatus(request):
    userr = request.user
    if userr.is_driver:
        driver = Driver.objects.get(user=userr)
        driver.on_road = not driver.on_road
        driver.save()
        return Response("Status changed", status=200)
    else:
        return Response("You are not a driver", status=403)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UploadUserDocuments(request):
    userr = request.user
    title = request.data.get('title')
    category = request.data.get('category')
    document=request.data.get('document')
    if not title:
        return Response("Title is required", status=400)
    if document == None:
        return Response("Document is required", status=400)
    document = Document.objects.create(user=userr, title=title, category=category, document=document)
    document.save()
    return Response("Document uploaded", status=200)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserDocumentsList(request, category=None):
    userr = request.user
    if category == None:
        documents = Document.objects.filter(user=userr)
    else:
        documents = Document.objects.filter(user=userr, category=category)
    documents_list = []
    for document in documents:
        document_json = {
            'id': document.id,
            'title': document.title,
            'document': document.document.url,
            'category': document.category
        }
        documents_list.append(document_json)
    return Response(documents_list, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteUserDocument(request):
    userr = request.user
    document_id = request.data.get('document_id')
    document = Document.objects.get(id=document_id)
    if document.user == userr or userr.is_dispatcher:
        document.document.delete(save=False)
        document.delete()
        return Response("Document deleted", status=200)
    else:
        return Response("You are not the owner of this document", status=403)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ChangeDocumentTitle(request):
    userr = request.user
    document_id = request.data.get('document_id')
    title = request.data.get('title')
    document = Document.objects.get(id=document_id)
    if document.user == userr or userr.is_dispatcher:
        document.title = title
        document.save()
        return Response("Title changed", status=200)
    else:
        return Response("You are not the owner of this document", status=403)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ReplaceDocument(request):
    userr = request.user
    document_id = request.data.get('document_id')
    document = Document.objects.get(id=document_id)
    if document.user == userr or userr.is_dispatcher:
        document.document.delete(save=False)
        document.document = request.data.get('document')
        document.save()
        return Response("Document replaced", status=200)
    else:
        return Response("You are not the owner of this document", status=403)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateRoute(request):
    userr = request.user
    if userr.is_dispatcher:
        driver_id = request.data.get('driver_id')
        current_date = date.today()
        driver = User.objects.get(id=driver_id)
        if driver.company != userr.company:
            return Response("Driver is not from the same company", status=400)
        route = Route.objects.create(driver=driver, dispatcher=userr, date=current_date)
        points = request.data.get('points', [])
        route.save()
        for point in points:
            name = point.get('name')
            latitude = point.get('latitude')
            longitude = point.get('longitude')
            point, created = Point.objects.get_or_create(name=name, latitude=latitude, longitude=longitude)
            route.points.add(point)
        return Response("Route created", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRoutes(request):
    userr = request.user
    if userr.is_dispatcher:
        routes = Route.objects.filter(dispatcher=userr)
    elif userr.is_driver:
        routes = Route.objects.filter(driver=userr)
    else:
        return Response("You are not authorized to view routes", status=403)

    current_date = date.today()
    routes_list = []
    for route in routes:
        if route.date == current_date:
            points_list = []
            for point in route.points.all():
                point_json = {
                    'name': point.name,
                    'latitude': point.latitude,
                    'longitude': point.longitude
                }
                points_list.append(point_json)
            route_json = {
                'id': route.id,
                'driver': route.driver.id,
                'dispatcher': route.dispatcher.id,
                'points': points_list,
                'date': route.date
            }
            routes_list.append(route_json)
    return Response(routes_list, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createDriver(request):
    userr = request.user
    if userr.is_dispatcher:
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')
        company = userr.company
        user = User.objects.create_user(email=email, name=name, password=password, company=company, is_driver=True, is_dispatcher=False)
        user.save()
        return Response("Driver created", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def numOfDrivers(request):
    userr = request.user
    if userr.is_dispatcher:
        drivers = User.objects.filter(company=userr.company, is_driver=True)
        return Response(len(drivers), status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transportAssignments(request):
    userr = request.user
    if userr.is_dispatcher:
        driver_id = request.data.get('driver_id')
        route_id = request.data.get('route_id')
        status_truck = request.data.get('status_truck')
        status_truck_text = request.data.get('status_truck_text')
        status_goods = request.data.get('status_goods')
        truck_combination = request.data.get('truck_combination')
        status_coupling = request.data.get('status_coupling')
        trailer_type = request.data.get('trailer_type')
        trailer_number = request.data.get('trailer_number')
        status_trailer_wagon = request.data.get('status_trailer_wagon')
        status_loaded_truck = request.data.get('status_loaded_truck')
        detraction = request.data.get('detraction')
        status_transport = request.data.get('status_transport', 'not started')
        documents = request.data.get('documents', [])

        driver = User.objects.get(id=driver_id)
        route = Route.objects.get(id=route_id)

        transport = Transport.objects.create(
            driver=driver,
            dispatcher=userr,
            route=route,
            status_truck=status_truck,
            status_truck_text=status_truck_text,
            status_goods=status_goods,
            truck_combination=truck_combination,
            status_coupling=status_coupling,
            trailer_type=trailer_type,
            trailer_number=trailer_number,
            status_trailer_wagon=status_trailer_wagon,
            status_loaded_truck=status_loaded_truck,
            detraction=detraction,
            status_transport=status_transport,
            documents=documents
        )
        transport.save()
        return Response("Transport created", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def transportUpdate(request):
    userr = request.user
    if userr.is_dispatcher:
        transport_id = request.data.get('transport_id')
        transport = Transport.objects.get(id=transport_id)
        if transport.dispatcher != userr:
            return Response("You are not the dispatcher of this transport", status=403)
        
        status_truck = request.data.get('status_truck')
        status_truck_text = request.data.get('status_truck_text')
        status_goods = request.data.get('status_goods')
        truck_combination = request.data.get('truck_combination')
        status_coupling = request.data.get('status_coupling')
        trailer_type = request.data.get('trailer_type')
        trailer_number = request.data.get('trailer_number')
        status_trailer_wagon = request.data.get('status_trailer_wagon')
        status_loaded_truck = request.data.get('status_loaded_truck')
        detraction = request.data.get('detraction')
        status_transport = request.data.get('status_transport')
        documents = request.data.get('documents', [])

        if status_truck is not None:
            transport.status_truck = status_truck
        if status_goods is not None:
            transport.status_goods = status_goods
        if status_truck_text is not None:
            transport.status_truck_text = status_truck_text
        if truck_combination is not None:
            transport.truck_combination = truck_combination
        if status_coupling is not None:
            transport.status_coupling = status_coupling
        if trailer_type is not None:
            transport.trailer_type = trailer_type
        if trailer_number is not None:
            transport.trailer_number = trailer_number
        if status_trailer_wagon is not None:
            transport.status_trailer_wagon = status_trailer_wagon
        if status_loaded_truck is not None:
            transport.status_loaded_truck = status_loaded_truck
        if detraction is not None:
            transport.detraction = detraction
        if status_transport is not None:
            transport.status_transport = status_transport
        if documents:
            new_documents = []
            new_documents.append(documents)
            new_documents.append(transport.documents)
            transport.documents = new_documents

        transport.save()
        return Response("Transport updated", status=200)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transportList(request):
    userr = request.user
    if userr.is_dispatcher:
        transports = Transport.objects.filter(dispatcher=userr)
    elif userr.is_driver:
        transports = Transport.objects.filter(driver=userr)
    else:
        return Response("You are not authorized to view transports", status=403)

    transports_list = []
    for transport in transports:
        route_points = []
        for point in transport.route.points.all():
            point_json = {
                'name': point.name,
                'latitude': point.latitude,
                'longitude': point.longitude
            }
            route_points.append(point_json)
        transport_json = {
            'id': transport.id,
            'driver': transport.driver.id,
            'dispatcher': transport.dispatcher.id,
            'route': route_points,
            'status_truck': transport.status_truck,
            'status_truck_text': transport.status_truck_text,
            'status_goods': transport.status_goods,
            'truck_combination': transport.truck_combination,
            'status_coupling': transport.status_coupling,
            'trailer_type': transport.trailer_type,
            'trailer_number': transport.trailer_number,
            'status_trailer_wagon': transport.status_trailer_wagon,
            'status_loaded_truck': transport.status_loaded_truck,
            'detraction': transport.detraction,
            'status_transport': transport.status_transport,
            'documents': transport.documents
        }
        transports_list.append(transport_json)
    return Response(transports_list, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def transportDelete(request):
    userr = request.user
    if userr.is_dispatcher:
        transport_id = request.data.get('transport_id')
        transport = Transport.objects.get(id=transport_id)
        if transport.dispatcher != userr:
            return Response("You are not the dispatcher of this transport", status=403)
        transport.delete()
        return Response("Transport deleted", status=200)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTransportDocument(request):
    userr = request.user
    if userr.is_dispatcher:
        transport_id = request.data.get('transport_id')
        transport = Transport.objects.get(id=transport_id)
        if transport.dispatcher != userr:
            return Response("You are not the dispatcher of this transport", status=403)
        document_id = request.data.get('document_id')
        transport_documents = transport.documents
        for document in transport_documents:
            if document['id'] == document_id:
                transport_documents.remove(document)
                break
        transport.documents = transport_documents
        transport.save()
        return Response("Document deleted", status=200)
    else:
        return Response("You are not a dispatcher", status=403)