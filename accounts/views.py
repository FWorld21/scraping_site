from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model
from . forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from django.contrib import messages

User = get_user_model()


# Create your views here.
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect("home")
    else:
        return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        messages.success(request, "Пользователь добавлен в систему!")
        return render(request, 'accounts/register_done.html', {'new_user': new_user})

    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data["city"]
                user.lang = data["lang"]
                user.send_email = data["send_email"]
                user.save()
                messages.success(request, "Данные сохранены")
                return redirect('accounts:update')
        form = UserUpdateForm(initial={'city': user.city, 'lang': user.lang, 'send_email': user.send_email})
        return render(request, 'accounts/update.html', {"form": form})
    else:
        return redirect("accounts:login")


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            queryset = User.objects.get(pk=user.pk)
            queryset.delete()
            messages.error(request, "Пользователь удалён!")
    return redirect("home")
