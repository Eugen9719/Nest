from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.forms import UserLoginForm, UserRegisterForm, UserEditForm, ProfileForm


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    next_page = reverse_lazy('shop:index')


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('user:login')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('shop:index')


@login_required
def profile(request):
    """
    Обрабатывает запросы на просмотр и редактирование профиля пользователя.
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Можно добавить сообщение об успешном сохранении
            messages.success(request, "Данные профиля успешно обновлены.")
        else:
            # Вывод ошибок валидации для отладки
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'messages': messages
    })
