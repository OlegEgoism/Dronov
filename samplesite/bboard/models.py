from django.db import models


class Bb(models.Model):
    KINDS = {
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    }
    kind = models.CharField(verbose_name='Позиции', max_length=1, choices=KINDS, blank=True) # default='s')
    rubric = models.ForeignKey('Rubric', verbose_name='Рубрика', on_delete=models.PROTECT, null=True)
    title = models.CharField(verbose_name='Товар', max_length=50)
    content = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.FloatField(verbose_name='Цена', null=True, blank=True)
    published = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Объявление'
        verbose_name = 'Объявления'
        ordering = ['-published']

    def __str__(self):
        return self.title


class Rubric(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20, db_index=True)

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name
