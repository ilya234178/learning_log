from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Главная страница приложения журнал обучения."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Добавляет новую тему"""
    if request.method != 'POST':
        #данные не отправлялись, создается пустая форма
        form = TopicForm()
    else:
        #отправлены данные POST, обработать данные
        form = TopicForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    #вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request,topic_id):
    """Добавляем новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #данные не отправлялись, создается пустая форма
        form = EntryForm()
    else:
        #отправлены данные 'POST', обработать данные
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit= False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #вывести пустую или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        #исходный запрос. форма заполняется даннымми текущей записи
        form = EntryForm(instance=entry)
    else:
        #отправка данных 'POST', обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)