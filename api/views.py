from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.serializers import UserCreateSerializerr
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.models import User, Driver, Dispatcher, Document
from base.models import Point, Route, Transport, TransportDocument, Truck, Trailer, TruckDocument, TrailerDocument, CMR
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
    transport = request.data.get('transport_id')
    if userr.is_dispatcher:
        try:
            transport = Transport.objects.get(id=transport)
        except Transport.DoesNotExist:
            return Response("Transport does not exist", status=404)
        current_date = date.today()
        route = Route.objects.create(transport=transport, date=current_date)
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
                'transport_id': route.transport.id,
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
def createTransport(request):
    userr = request.user
    if userr.is_dispatcher:
        driver_id = request.data.get('driver_id')
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
        truck = request.data.get('truck_id')
        trailer = request.data.get('trailer_id')

        driver = User.objects.get(id=driver_id)

        transport = Transport.objects.create(
            driver=driver,
            dispatcher=userr,
            truck=truck,
            trailer=trailer,
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
        )
        transport.save()
        return Response("Transport created", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UploadTransportDocuments(request):
    transport = request.data.get('transport_id')
    title = request.data.get('title')
    category = request.data.get('category')
    document=request.data.get('document')
    try:
        transport = Transport.objects.get(id=transport)
    except Transport.DoesNotExist:
        return Response("Transport does not exist", status=404)

    if not title:
        return Response("Title is required", status=400)
    if document == None:
        return Response("Document is required", status=400)
    document = TransportDocument.objects.create(transport=transport, title=title, category=category, document=document)
    document.save()
    return Response("Document uploaded", status=200)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def transportUpdate(request):
    transport_id = request.data.get('transport_id')
    transport = Transport.objects.get(id=transport_id)
        
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
    truck = request.data.get('truck_id')
    trailer = request.data.get('trailer_id')

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
    if truck is not None:
            transport.truck = truck
    if trailer is not None:
            transport.trailer = trailer

    transport.save()
    return Response("Transport updated", status=200)

@api_view(['DELETE']) #todo: documents only from trasnports you are assigned to
@permission_classes([IsAuthenticated])
def deleteTransportDocument(request):
    transport = request.data.get('transport_id')
    document_id = request.data.get('document_id')
    document = TransportDocument.objects.get(transport=transport, id=document_id)
    document.document.delete(save=False)
    document.delete()
    return Response("Document deleted", status=200)
    

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
        route_list = []
        route_points = []
        documents_list = []
        
        route_list = Route.objects.filter(transport=transport)

        if route_list.exists():
            for route in route_list:
                points_list = []
                route_points = route.points.all()
                for point in route_points:
                    point_json = {
                        'name': point.name,
                        'latitude': point.latitude,
                        'longitude': point.longitude
                    }
                    points_list.append(point_json)

        documents = TransportDocument.objects.filter(transport=transport)
            
        for document in documents:
            document_json = {
                'id': document.id,
                'title': document.title,
                'document': document.document.url,
                'category': document.category
            }
            documents_list.append(document_json)

        transport_json = {
            'id': transport.id,
            'driver': transport.driver.id,
            'truck': transport.truck.id if transport.truck else None,
            'trailer': transport.trailer.id if transport.trailer else None,
            'dispatcher': transport.dispatcher.id,
            'route': points_list,
            'route_date': route_list[0].date if route_list.exists() else None, #to be discussed
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
            'documents': documents_list
        }
        transports_list.append(transport_json)
    return Response(transports_list, status=200)

@api_view(['DELETE']) #todo: can delete only transports you are assigned to
@permission_classes([IsAuthenticated])
def transportDelete(request):
    userr = request.user
    if userr.is_dispatcher:
        transport_id = request.data.get('transport_id')
        transport = Transport.objects.get(id=transport_id)
        if transport.dispatcher != userr:
            return Response("You are not the dispatcher of this transport", status=403)
        
        documents = TransportDocument.objects.filter(transport=transport)
        for document in documents:
            document.document.delete(save=False)
            document.delete()

        transport.delete()
        return Response("Transport deleted", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCMR(request):
    userr = request.user
    if userr.is_dispatcher or userr.is_driver:
        transport_id = request.data.get('transport_id')
        driver_id = request.data.get('driver_id')
        expeditor_nume = request.data.get('expeditor_nume')
        expeditor_adresa = request.data.get('expeditor_adresa')
        expeditor_tara = request.data.get('expeditor_tara')
        destinatar_nume = request.data.get('destinatar_nume')
        destinatar_adresa = request.data.get('destinatar_adresa')
        destinatar_tara = request.data.get('destinatar_tara')
        loc_livrare = request.data.get('loc_livrare')
        loc_incarcare = request.data.get('loc_incarcare')
        data_incarcare = request.data.get('data_incarcare')
        marci_numere = request.data.get('marci_numere')
        numar_colete = request.data.get('numar_colete')
        mod_ambalare = request.data.get('mod_ambalare')
        natura_marfii = request.data.get('natura_marfii')
        nr_static = request.data.get('nr_static')
        greutate_bruta = request.data.get('greutate_bruta')
        cubaj = request.data.get('cubaj')
        instructiuni_expeditor = request.data.get('instructiuni_expeditor')
        conventii_speciale = request.data.get('conventii_speciale')

        try:
            transport = Transport.objects.get(id=transport_id)
        except Transport.DoesNotExist:
            return Response({"error": "Transport does not exist"}, status=404)

        driver = None
        if driver_id:
            try:
                driver = User.objects.get(id=driver_id)
            except User.DoesNotExist:
                return Response({"error": "Driver does not exist"}, status=404)

        cmr = CMR.objects.create(
            transport=transport,
            driver=driver,
            dispatcher=userr,
            expeditor_nume=expeditor_nume,
            expeditor_adresa=expeditor_adresa,
            expeditor_tara=expeditor_tara,
            destinatar_nume=destinatar_nume,
            destinatar_adresa=destinatar_adresa,
            destinatar_tara=destinatar_tara,
            loc_livrare=loc_livrare,
            loc_incarcare=loc_incarcare,
            data_incarcare=data_incarcare if data_incarcare else date.today(),
            marci_numere=marci_numere,
            numar_colete=numar_colete,
            mod_ambalare=mod_ambalare,
            natura_marfii=natura_marfii,
            nr_static=nr_static,
            greutate_bruta=greutate_bruta,
            cubaj=cubaj,
            instructiuni_expeditor=instructiuni_expeditor,
            conventii_speciale=conventii_speciale
        )
        cmr.save()
        return Response({"message": "CMR added successfully"}, status=200)
    else:
        return Response({"error": "You are not authorized to add a CMR"}, status=403)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCMR(request):
    userr = request.user
    cmr_id = request.data.get('cmr_id')
    try:
        cmr = CMR.objects.get(id=cmr_id)
    except CMR.DoesNotExist:
        return Response("CMR does not exist", status=404)

    if cmr.transport.dispatcher == userr or cmr.driver == userr:
        cmr.delete()
        return Response("CMR deleted successfully", status=200)
    else:
        return Response("You are not authorized to delete this CMR", status=403)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCMR(request):
    userr = request.user
    cmr_id = request.data.get('cmr_id')
    try:
        cmr = CMR.objects.get(id=cmr_id)
    except CMR.DoesNotExist:
        return Response("CMR does not exist", status=404)

    if cmr.transport.dispatcher == userr or cmr.driver == userr:
        fields_to_update = [
            'expeditor_nume', 'expeditor_adresa', 'expeditor_tara',
            'destinatar_nume', 'destinatar_adresa', 'destinatar_tara',
            'loc_livrare', 'loc_incarcare', 'data_incarcare',
            'marci_numere', 'numar_colete', 'mod_ambalare',
            'natura_marfii', 'nr_static', 'greutate_bruta',
            'cubaj', 'instructiuni_expeditor', 'conventii_speciale'
        ]

        for field in fields_to_update:
            if field in request.data:
                setattr(cmr, field, request.data.get(field))

        cmr.save()
        return Response("CMR updated successfully", status=200)
    else:
        return Response("You are not authorized to update this CMR", status=403)

def addTruck(request):
    userr = request.user
    company = userr.company
    if userr.is_dispatcher:
        license_plate = request.data.get('license_plate')
        vin = request.data.get('vin')
        make = request.data.get('make')
        model = request.data.get('model')
        year = request.data.get('year')
        next_service_date = request.data.get('next_service_date')
        last_service_date = request.data.get('last_service_date')

        truck = Truck.objects.create(
            license_plate=license_plate,
            vin=vin,
            company=company,
            make=make,
            model=model,
            year=year,
            next_service_date=next_service_date,
            last_service_date=last_service_date
        )
        truck.save()
        return Response("Truck added", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UploadTruckDocuments(request):
    truck = request.data.get('truck_id')
    title = request.data.get('title')
    category = request.data.get('category')
    document=request.data.get('document')
    try:
        truck = Truck.objects.get(id=truck)
    except Truck.DoesNotExist:
        return Response("Truck does not exist", status=404)

    if not title:
        return Response("Title is required", status=400)
    if document == None:
        return Response("Document is required", status=400)
    document = TruckDocument.objects.create(truck=truck, title=title, category=category, document=document)
    document.save()
    return Response("Document uploaded", status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTruck(request):
    userr = request.user
    if userr.is_dispatcher:
        truck_id = request.data.get('truck_id')
        truck = Truck.objects.get(id=truck_id)

        documents = TruckDocument.objects.filter(truck=truck)
        for document in documents:
            document.document.delete(save=False)
            document.delete()

        truck.delete()
        return Response("Truck deleted", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllTrucks(request):
    userr = request.user
    if userr.is_dispatcher:
        trucks = Truck.objects.filter(company=userr.company)
        trucks_list = []
        for truck in trucks:
            truck_json = {
                'id': truck.id,
                'license_plate': truck.license_plate,
                'vin': truck.vin,
                'make': truck.make,
                'model': truck.model,
                'year': truck.year,
                'next_service_date': truck.next_service_date,
                'last_service_date': truck.last_service_date
            }
            trucks_list.append(truck_json)
        return Response(trucks_list, status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addTrailer(request):
    userr = request.user
    company = userr.company
    if userr.is_dispatcher:
        license_plate = request.data.get('license_plate')
        vin = request.data.get('vin')
        make = request.data.get('make')
        model = request.data.get('model')
        year = request.data.get('year')
        next_service_date = request.data.get('next_service_date')
        last_service_date = request.data.get('last_service_date')

        trailer = Trailer.objects.create(
            license_plate=license_plate,
            vin=vin,
            company=company,
            make=make,
            model=model,
            year=year,
            next_service_date=next_service_date,
            last_service_date=last_service_date
        )
        trailer.save()
        return Response("Trailer added", status=200)
    else:
        return Response("You are not a dispatcher", status=403)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTrailer(request):
    userr = request.user
    if userr.is_dispatcher:
        trailer_id = request.data.get('trailer_id')
        trailer = Trailer.objects.get(id=trailer_id)

        documents = TrailerDocument.objects.filter(trailer=trailer)
        for document in documents:
            document.document.delete(save=False)
            document.delete()

        trailer.delete()
        return Response("Trailer deleted", status=200)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllTrailers(request):
    userr = request.user
    if userr.is_dispatcher:
        trailers = Trailer.objects.filter(company=userr.company)
        trailers_list = []
        for trailer in trailers:
            trailer_json = {
                'id': trailer.id,
                'license_plate': trailer.license_plate,
                'vin': trailer.vin,
                'make': trailer.make,
                'model': trailer.model,
                'year': trailer.year,
                'next_service_date': trailer.next_service_date,
                'last_service_date': trailer.last_service_date
            }
            trailers_list.append(trailer_json)
        return Response(trailers_list, status=200)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latestNTransports(request, n, driver_id):
    #n = request.query_params.get('n', 5)  # Default to 5 if 'n' is not provided
    userr = request.user
    if userr.is_dispatcher:
        #driver_id = request.query_params.get('driver_id')
        try:
            driver = User.objects.get(id=driver_id, is_driver=True, company=userr.company)
        except User.DoesNotExist:
            return Response("Driver does not exist or is not part of your company", status=404)
        transports = Transport.objects.filter(dispatcher=userr, driver=driver).order_by('-id')[:n]
    elif userr.is_driver:
        transports = Transport.objects.filter(driver=userr).order_by('-id')[:n]
    else:
        return Response("You are not authorized to view transports", status=403)

    transports_list = []
    for transport in transports:
        transport_json = {
            'id': transport.id,
            'driver': transport.driver.id,
            'truck': transport.truck.id if transport.truck else None,
            'trailer': transport.trailer.id if transport.trailer else None,
            'dispatcher': transport.dispatcher.id,
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
        }
        transports_list.append(transport_json)
    return Response(transports_list, status=200)