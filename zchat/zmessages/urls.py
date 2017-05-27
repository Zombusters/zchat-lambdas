"""zmessages API URL Configuration."""
from django.conf.urls import url, include
from rest_framework import routers

from .serializers import (
    MessageViewSet, MyMessageViewSet,
    MyMobilePushTokenViewSet,
    UserViewSet, AddUserView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'messages', MessageViewSet, base_name='messages')
router.register(r'my-messages', MyMessageViewSet, base_name='my-messages')
router.register(r'my-token', MyMobilePushTokenViewSet, base_name='my-token')


urlpatterns = [
    url(r'^add-user', AddUserView.as_view(), name='add-new-user'),
    url(r'^', include(router.urls)),
]
