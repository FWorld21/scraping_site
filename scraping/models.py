from django.db import models
from . ru_to_eng import translate
import jsonfield


def default_urls():
    return {"work": "", "rabota": "", "dou": "", "djinni": ""}


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название города", unique=True)
    slug = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translate(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name="Язык программирования", unique=True)
    slug = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    company = models.CharField(max_length=30)
    url = models.URLField(unique=True)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Errors(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()


class Url(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="Город")
    lang = models.ForeignKey("Language", on_delete=models.CASCADE, verbose_name="Язык программирования")
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "lang")

