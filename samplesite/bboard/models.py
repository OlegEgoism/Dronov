from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


def min_length():
    min_length = 0
    return min_length


def validate_even(vol):
    if vol < 0:
        raise ValidationError('Число %(value)s некоректное', code='odd', params={'value': vol})


# class MinMaxVaiueVaiidator:
#     def __init__(self, min_value, max_value):
#         self.min_value = min_value
#         self.max_value = max_value
#
#     def __call__(self, vol):
#         if vol < self.min_value or vol > self.max_value:
#             raise ValidationError('Введенное число должно' + 'находиться в диапазоне от % (min) s до % (max) s',
#                                   code='out_of_range', params={'min': self.min_value, 'max': self.max_value})


# class BbManager(models.Manager):
#     """
#     Создание диспетчеров обратной связи
#     """
#
#     def get_queryset(self):
#         return super().get_queryset().order_by('price')


class Bb(models.Model):
    KINDS = {
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    }
    kind = models.CharField(verbose_name='Позиции', max_length=1, choices=KINDS, blank=True)
    rubric = models.ForeignKey('Rubric', verbose_name='Рубрика', on_delete=models.CASCADE, null=True, related_name='+')
    title = models.CharField(verbose_name='Товар', max_length=50,
                             validators=[validators.MinLengthValidator(min_length)],
                             error_messages={'min_length': 'Неправильно, должно быть миинимум 1 символ'})
    content = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, null=True, blank=True,
                                validators=[validate_even])
    published = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, db_index=True)

    # objects = models.Manager()
    # by_price = BbManager()

    class Meta:
        verbose_name_plural = 'Объявление'
        verbose_name = 'Объявления'
        ordering = ['-published']

    def __str__(self):
        return self.title

    def title_and_price(self):
        """Соединят строки title и price"""
        if self.price:
            return '%s (цена: %.f р.)' % (self.title, self.price)
        else:
            return self.title

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите опписание товара')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите не отрицательное значение цены')

        if errors:
            raise ValidationError(errors)


class RubricManager(models.Manager):
    """
    Создание диспетчеров записей
    """

    def get_queryset(self):
        return super().get_queryset().order_by('id')

    def order_by_bb_count(self):
        return super().get_queryset().annotate(cnt=models.Count('bb')).order_by('-cnt')


class Rubric(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20, db_index=True)
    objects = models.Manager()
    bbs = RubricManager()

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name


# class RubricQuerySet(models.QuerySet):
#     """
#     Создание своих наборов записей
#     """
#
#     def order_count(self):
#         return self.annotate(cnt=models.Count('bb')).order_by('pk')


class AdvUser(models.Model):
    is_activated = models.BooleanField(verbose_name='Активнвация', default=True)
    user = models.OneToOneField(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'


class Spare(models.Model):
    name = models.CharField(verbose_name='Детали', max_length=50)

    class Meta:
        verbose_name_plural = 'Детали'
        verbose_name = 'Деталь'

    def __str__(self):
        return self.name


class Mashine(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    spares = models.ManyToManyField(Spare, verbose_name='Детали')
    notes = GenericRelation('Note')

    class Meta:
        verbose_name_plural = 'Машина'
        verbose_name = 'Машины'

    def __str__(self):
        return self.name


class Kit(models.Model):
    mashines = models.ForeignKey(Mashine, verbose_name='Машина', on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, verbose_name='Детали', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', validators=[validate_even])

    class Meta:
        verbose_name_plural = 'Запчасть'
        verbose_name = 'Запчасти'

    def __str__(self):
        return self.mashines


class Note(models.Model):
    """
    Полиморфная связь
    """
    content = models.TextField(verbose_name='Содержание')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Содержание связи')
    object_id = models.PositiveIntegerField(verbose_name='Колличество объектов')
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        verbose_name_plural = 'Полиморфная связь'
        verbose_name = 'Полиморфная связь'


class Messages(models.Model):
    """
    Прямое наследование
    """
    content = models.TextField(verbose_name='Содержание')
    name = models.CharField(verbose_name='Имя', max_length=200)
    email = models.EmailField(verbose_name='Почта')

    class Meta:
        verbose_name_plural = '-Сообщения'
        verbose_name = '-Сообщение'

    # class Meta:
    #     abstract = True
    #     ordering = ['name']


class PrivateMessages(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    message = models.OneToOneField(Messages, verbose_name='Сообщение', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя', max_length=40)
    email = None

    class Meta:
        verbose_name_plural = '-Приватные сообщения'
        verbose_name = '-Приватное сообщение'

    def __str__(self):
        return self.name

    # class Meta (Messages.Meta):
    #     pass


class RevRubric(Rubric):
    class Meta:
        proxy = True
        ordering = ['name']
