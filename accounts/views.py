from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Регистрирует нового пользователя."""
    if request.method != "POST":
        #вывод пустой формы регистрации
        form = UserCreationForm()
    else:
        #Обработка заполненной формы
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:index')

    #вывод пустой или недействительной формы
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


