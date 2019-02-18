from django.conf.urls import url
from .consumers import LikeAddConsumer
from .consumers import CountUserConsumer

websocket_urlpatterns = [
    url(r'^ws/like/add/$', LikeAddConsumer ),
    url(r'^ws/users/$', CountUserConsumer),
]