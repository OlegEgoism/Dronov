from django.contrib import admin

from django.db import models
from django import forms
from django.urls import reverse

from .models import Bb, Rubric, AdvUser, Mashine, Spare, Kit, Note, PrivateMessages, Messages


class PriceListFilter(admin.SimpleListFilter):  # Собственная фильтрация объявлений
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Низкая цена: до 100'),
            ('medium', 'Средняя цена: 100-150'),
            ('high', 'Высокая цена: от 150'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=100)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=100, price__lte=150)
        elif self.value() == 'high':
            return queryset.filter(price__gt=150)


class BbAdmina(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     else:
    #         return qs.filter(is_hidden=False)

    # formfield_overrides = {models.ForeignKey: {'widget': forms.widgets.Select(attrs={'size': 430})}, }

    def view_on_site(self, rec):
        return reverse('detail', kwargs={'pk': rec.pk})

    def get_list_display(self, request):
        id = ['title', 'content', 'price']
        if request.user.is_superuser:
            id += ['published', 'rubric']
        return id

    def get_list_display_links(self, request, list_display):
        return list_display

    list_filter = (PriceListFilter,)
    date_hierarchy = 'published'
    list_per_page = 5  # количество записей в части пагинатора
    list_max_show_all = 20  # количество записей, которые появятся на странице списка после щелчка на гиперссылке Показать все
    actions_on_top = True
    # radio_fields = {'rubric': admin.VERTICAL}
    # prepopulated_fields = {"slug": ("title",)}

    # list_display = 'title', 'content', 'price', 'published', 'rubric', 'kind', 'title_and_rubric'
    # list_display_links = 'title', 'rubric'
    # search_fields = 'title', 'content'
    # list_filter = 'rubric', 'kind'
    #
    #
    # def title_and_rubric(self, rec):  # состав выводимого списка
    #     return '%s (%s)' % (rec.title, rec.price)
    # title_and_rubric.short_description = 'Назавание и цена'


class RubricAdmin(admin.ModelAdmin):
    list_display = 'name',


class MashineAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    # filter_horizontal = ('spares', )
    filter_vertical = ('spares',)


class SpareAdmin(admin.ModelAdmin):
    list_display = ['name']


class KitAdmin(admin.ModelAdmin):
    list_display = 'mashines', 'spare', 'count'
    list_editable = 'count',
    readonly_fields = 'mashines',


class NoteAdmin(admin.ModelAdmin):
    list_display = 'content', 'content_type', 'object_id'


admin.site.register(Bb, BbAdmina)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(AdvUser)
admin.site.register(Mashine, MashineAdmin)
admin.site.register(Spare, SpareAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(PrivateMessages)
admin.site.register(Messages)
