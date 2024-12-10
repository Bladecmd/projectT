from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.response import Response
from rest_framework.status import *

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout

# imports for auth
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# import Author from data_api & AuthorSerializer
from data_api_app.models import Author
from .serializers import AuthorSerializer


# TODO wrap the functions is similar classes as the data_api view
# TODO investigate if needed to upgrade to class based views
# TODO api key auth
# TODO investigate OTP validation


# Create your views here.
@api_view(["POST"])
def signup(request):
    serializer = AuthorSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        # author as a response
        author = Author.objects.get(username=request.data['username'])
        token = Token.objects.get(user=author)
        
        serializer = AuthorSerializer(author)
        data = {
            "author": serializer.data,
            "token": token.key
        }
        
        return Response(data, status=HTTP_201_CREATED)
    
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    
    data = request.data
    authenticated_user = authenticate(username=data["username"], password=data['password'])
    
    if authenticated_user is None:
        return Response({"error": "Invalid username/password"}, status=HTTP_400_BAD_REQUEST)
    
    # if the user is authenticated do the below
    author = Author.objects.get(username=data['username'])
    serializer = AuthorSerializer(author)
    
    existing_token, new_token = Token.objects.get_or_create(user=author)

    data = {
        "author": serializer.data,
        # we can do logical operator short-circuiting in Python as well...
        "token": existing_token.key or new_token.key
    }
    return Response(data, status=HTTP_200_OK)
    

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    
    # _request needed as DRF wraps the request and we need the original request - can't do logout without it
    logout(request._request)
    request.user.auth_token.delete()
    
    return Response({"message": "logged out"}, status=HTTP_200_OK)
