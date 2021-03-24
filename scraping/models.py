from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название города")
    slug = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
