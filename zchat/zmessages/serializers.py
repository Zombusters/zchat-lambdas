from django.contrib.auth.models import User

from zchat.permissions import IsOwnerOrReadOnly
from zmessages.models import Message
from rest_framework import routers, serializers, viewsets, permissions


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
