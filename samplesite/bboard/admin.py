from django.contrib import admin

from .models import Bb, Rubric


class BbAdmina(admin.ModelAdmin):
    list_display = 'title', 'content', 'price', 'published', 'rubric', 'kind'
    list_display_links = 'title', 'rubric'
    search_fields = 'title', 'content'
    list_filter = 'rubric', 'kind'


class RubricAdmin(admin.ModelAdmin):
    list_display = 'name',


admin.site.register(Bb, BbAdmina)
admin.site.register(Rubric, RubricAdmin)
