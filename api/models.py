from django.db import models

from .validators import validate_title_year

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[validate_title_year], blank=True)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField('Genre', blank=True, related_name='titles')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True,  blank=True, related_name='titles')

    class Meta:
        ordering = ['-id',]

    def __str__(self):
        return self.name
