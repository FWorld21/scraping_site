from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            queryset = User.objects.filter(email=email)
            if not queryset.exists():
                raise forms.ValidationError("Такого пользователя не существует.")
            if not check_password(password=password, encoded=queryset[0].password):
                raise forms.ValidationError("Пароль не верный.")
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Данный аккаунт отключён.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Введите свою почту", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Введите новый пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('email', )
        # Все методы, которые начинаются на слово clean в формах, будут вызываться в любом случае.

    def clean_password2(self):
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        else:
            return data["password2"]


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="slug", required=True,
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  label="Город"
                                  )
    lang = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name="slug", required=True,
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  label="Язык программирования"
                                  )
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="Получать рассылку?")

    class Meta:
        model = User
        fields = ('city', 'lang', 'send_email')
