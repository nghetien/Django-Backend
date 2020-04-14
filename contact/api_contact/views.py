from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from contact.api_contact.serializers import ContactSerializers



@api_view(['POST',])
def contact_api(request):
    message = {}
    if request.method =="POST":
        serializers = ContactSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            message['status'] = status.HTTP_201_CREATED
            message['message'] = "OK"
            data = serializers.data
            message['data'] = data
            return Response(message)
        else:
            print("----------------------",serializers.errors)
            message['status'] = status.HTTP_400_BAD_REQUEST
            your_error = serializers.errors
            error = your_error.values()
            for item in error:
                fail = item[0]
                break
            message['message'] = fail
            message['data'] = "null"
            return Response(message)
