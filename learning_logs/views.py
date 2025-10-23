from django.shortcuts import render

def index(request):
    """Главная страница приложения журнал обучения."""
    return render(request, 'learning_logs/index.html')