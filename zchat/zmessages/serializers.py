from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import serializers, viewsets, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from zchat.permissions import IsOwnerOrReadOnly
from zmessages.models import Message, MobilePushToken, Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('author', 'msg', 'timestamp')


class MyMessageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Message
        fields = ('msg', 'timestamp')


class MyMobilePushTokenSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MobilePushToken
        fields = ('token', 'timestamp')


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=254, min_length=5)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'username', 'email', 'is_staff')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        extra_kwargs = {'creator': {'read_only': True}}


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class MyMessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MyMessageSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Message.objects.all().filter(author=self.request.user.id)
        return queryset


class MyMobilePushTokenViewSet(viewsets.ModelViewSet):
    serializer_class = MyMobilePushTokenSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return (
            self.serializer_class.Meta.
            model.objects.all().
            filter(user_id=self.request.user.id)
        )


class AddUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        serializer.save(password=password)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
