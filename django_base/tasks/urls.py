from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.message_board, name='message_board'),
    path('status/<uuid:task_id>/', views.task_status, name='task_status'),
    path('send_message/', views.send_message, name='send_message'),
]