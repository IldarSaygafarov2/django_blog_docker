from django.db import models

# Create your models here.

# MVT


class BaseTimedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Дата обновления')

    class Meta:
        abstract = True # говорит,что данный класс, не используется в базе данных