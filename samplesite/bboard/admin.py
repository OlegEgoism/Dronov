from django.contrib import admin

from .models import Bb, Rubric, AdvUser, Mashine, Spare, Kit, Note, PrivateMessages, Messages


class BbAdmina(admin.ModelAdmin):
    list_display = 'title', 'content', 'price', 'published', 'rubric', 'kind'
    list_display_links = 'title', 'rubric'
    search_fields = 'title', 'content'
    list_filter = 'rubric', 'kind'


class RubricAdmin(admin.ModelAdmin):
    list_display = 'name',


class MashineAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


class SpareAdmin(admin.ModelAdmin):
    list_display = ['name']


class KitAdmin(admin.ModelAdmin):
    list_display = 'mashines', 'spare', 'count'
    list_editable = 'count',


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
