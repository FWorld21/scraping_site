from django.db import models
from . ru_to_eng import translate


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
