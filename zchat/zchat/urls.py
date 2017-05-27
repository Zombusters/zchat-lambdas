"""zchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token, obtain_jwt_token
from zmessages.serializers import MessageViewSet, MyMessageViewSet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'username', 'email', 'is_staff')


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=254, min_length=5)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = NewUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        serializer.save(password=password)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'messages', MessageViewSet, base_name='messages')
router.register(r'my-messages', MyMessageViewSet, base_name='my-messages')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-add-user', AddUserView.as_view(), name='add-new-user'),
    # jwt
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
