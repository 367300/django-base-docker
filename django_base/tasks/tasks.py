from celery import shared_task
from .models import TaskStatus
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Message
import requests

def send_status_update(task_id, status, result=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'task_{task_id}',
        {
            'type': 'task_status_update',
            'status': status,
            'result': result,
        }
    )

def update_status(task_id, status, result=None):
    try:
        task = TaskStatus.objects.get(id=task_id)
        task.status = status
        if result is not None:
            task.result = result
        task.save()
        send_status_update(task_id, status, result)
    except TaskStatus.DoesNotExist:
        pass

@shared_task(bind=True)
def long_task(self, task_id):
    update_status(task_id, 'STARTED')
    # Имитируем бурную деятельность
    time.sleep(5)
    update_status(task_id, 'SUCCESS', result='Готово!')
    return 'Готово!'

@shared_task(bind=True)
def classify_message_category(self, message_id):
    try:
        msg = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return
    try:
        response = requests.post(
            'http://172.17.0.1:5001/predict',
            json={'text': msg.text},
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            category = data.get('category')
            if category:
                msg.category = category
                msg.save()
                # Отправить обновление по WebSocket
                send_message_update(str(msg.id), category)
    except Exception:
        pass

def send_message_update(message_id, category):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'message_{message_id}',
        {
            'type': 'message_category_update',
            'category': category,
        }
    )
