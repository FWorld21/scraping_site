from django import forms
from scraping.models import City, Language


class FormForSearch(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="slug",
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  label="Город"
                                  )
    lang = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name="slug", required=False,
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  label="Язык программирования"
                                  )
