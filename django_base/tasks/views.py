from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskStatus
from .tasks import long_task
from django.http import JsonResponse
from .models import Message
import requests
from .tasks import classify_message_category

def task_form(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # Создаём объект статуса задачи
        task_status = TaskStatus.objects.create()  # type: ignore
        if action == 'sync':
            # Синхронное выполнение
            long_task(str(task_status.id))
            return redirect('tasks:task_status', task_id=task_status.id)
        elif action == 'async':
            # Асинхронное выполнение через Celery
            long_task.delay(str(task_status.id))
            return redirect('tasks:task_status', task_id=task_status.id)
    return render(request, 'tasks/task_form.html')

def task_status(request, task_id):
    task = get_object_or_404(TaskStatus, id=task_id)  # type: ignore
    return render(request, 'tasks/task_status.html', {'task': task})

def send_message(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text:
            return JsonResponse({'error': 'Пустое сообщение'}, status=400)
        # Сохраняем сообщение без категории
        msg = Message.objects.create(text=text)
        # Проверяем доступность ML-сервиса
        try:
            health = requests.get('http://172.17.0.1:5001/health', timeout=1)
            if health.status_code == 200 and health.json().get('status'):
                # Ставим задачу на определение категории
                classify_message_category(str(msg.id))
        except Exception:
            pass  # ML-сервис недоступен, категорию не определяем
        return JsonResponse({'id': str(msg.id), 'text': msg.text, 'category': msg.category, 'created': msg.created})
    return JsonResponse({'error': 'Только POST'}, status=405)

def message_board(request):
    messages = Message.objects.order_by('-created')[:50]
    return render(request, 'tasks/message_board.html', {'messages': messages})
