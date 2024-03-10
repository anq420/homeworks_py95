from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.db.models import Q
from blog.forms import RegistrationForm


User = get_user_model()


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


def sign_up_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            user = User.objects.filter(Q(email=email) | Q(username=username))

            if not user and password == confirm_password:
                user_ = User.objects.create_user(email=email, username=username, password=confirm_password)
                messages.success(request, 'Успешная регистрация')
                return redirect('main')

            if user:
                messages.error(request, 'Такая почта или никнейм уже используются')

            if password != confirm_password:
                messages.error(request, "Проверьте правильность введённого пароля и попробуйте ещё раз")
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def sign_in_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            u_pass = user.check_password(password)

            if user and u_pass:
                login(request, user)
                messages.success(request, 'Успешный вход')
                return redirect('main')
            else:
                messages.error(request, 'Неверный пароль')

        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким адресом электронной почты не найден')

    return render(request, 'login.html')
