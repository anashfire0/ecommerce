import random
import string

from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    new_order_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id


def unique_slug_generator(instance, new_slug=None):
    slug = new_slug if new_slug else slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{random_string_generator(4)}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
