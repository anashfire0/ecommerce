from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from django.urls import reverse

from ecommerce.utils import unique_slug_generator

import random
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    print(instance)
    new_filename = random.randint(0, 9999)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}'


class ProductQuerySet(QuerySet):

    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookup = (Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(price__contains=query)|
                  Q(tags__title__contains=query)
                  )
        return self.filter(lookup).active().distinct()

class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    title = models.CharField('Title', max_length=120)
    slug = models.SlugField(blank=True)
    description = models.TextField('Description')
    price = models.DecimalField(
        'Price', max_digits=10, decimal_places=2, default=19.99)
    image = models.ImageField(
        'Image', upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug,])



def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)


