from django.urls import re_path
from .consumers import TaskStatusConsumer, MessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/tasks/status/(?P<task_id>[0-9a-f-]+)/$', TaskStatusConsumer.as_asgi()),
    re_path(r'ws/tasks/message/(?P<message_id>[0-9a-f-]+)/$', MessageConsumer.as_asgi()),
] 