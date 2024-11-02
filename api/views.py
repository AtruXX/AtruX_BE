from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.serializers import UserCreateSerializerr
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDrivers(request):
    userr = request.user
    if userr.is_dispatcher:
        drivers = User.objects.filter(company=userr.company, is_driver=True)
        driver_list = []
        for driver in drivers:
            driver_json = {
                'id': driver.id,
                'email': driver.email,
                'name': driver.name,
                'company': driver.company.name,
                'is_dispatcher': driver.is_dispatcher,
                'is_driver': driver.is_driver
            }
            driver_list.append(driver_json)
        driver_data = UserCreateSerializerr(driver_list, many=True).data
        return Response(driver_data)
    else:
        return Response("You are not a dispatcher", status=403)
