from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.serializers import UserCreateSerializerr
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.models import User, Driver, Dispatcher

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDrivers(request):
    userr = request.user
    if userr.is_dispatcher:
        drivers = User.objects.filter(company=userr.company, is_driver=True)
        driver_list = []
        for driver in drivers:
            ddriver = Driver.objects.get(company=userr.company)
            rating = ddriver.rating / ddriver.nr_of_ratings
            driver_json = {
                'id': driver.id,
                'email': driver.email,
                'name': driver.name,
                'company': driver.company.name,
                'is_dispatcher': driver.is_dispatcher,
                'is_driver': driver.is_driver,
                'rating' : rating,
                'on_road': ddriver.on_road
            }
            driver_list.append(driver_json)
        driver_data = UserCreateSerializerr(driver_list, many=True).data
        return Response(driver_data)
    else:
        return Response("You are not a dispatcher", status=403)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfile(request):
    userr = request.user
    if userr.is_driver:
        driver = Driver.objects.get(user=userr)
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