from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .renderers import UserJSONRenderer
from .models import Profile, User

from .serializers import ProfileSerializer, RegistrationSerializer, ModeratorRegistrationSerializer, LoginSerializer, UserSerializer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data['token'], headers={'x-auth-token':serializer.data['token']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       

class ModeratorRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ModeratorRegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data['token'], headers={'x-auth-token':serializer.data['token']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        print(user)
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            print(serializer.data['token'])
            return Response(serializer.data['token'])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



class ProfileDetailView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    
    def get(self, request, user_email, format=None):
        the_user = get_object_or_404(User,email=user_email)
        the_profile = get_object_or_404(Profile,user=the_user)
        serializer = ProfileSerializer(the_profile)
        return Response(serializer.data)

    
    def patch(self, request, user_email, format=None):
        photo_file = request.data['photo']
        print(photo_file)
        the_user = get_object_or_404(User,email=user_email)
        the_profile = get_object_or_404(Profile,user=the_user)
        print(the_profile)
       
        serializer = ProfileSerializer(the_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)