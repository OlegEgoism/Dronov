from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.dates import ArchiveIndexView, YearMixin, MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import BbForm
from .models import Bb, Rubric


def index(request):
    bbs = Bb.objects.all()
    rubric = Rubric.objects.all()
    paginator = Paginator(bbs, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        'bbs': page.object_list,
        'rubric': rubric,
        'page': page,
    }
    return render(request, template_name='bboard/index.html', context=context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubirc = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubric': rubirc,
        'current_rubric': current_rubric
    }
    return render(request, template_name='bboard/by_rubric.html', context=context)


class BbDetailView(DetailView):
    model = Bb

    def get_contex_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


# class BbByRubricView(ListView):
#     template_name = 'bboard/by_rubric.html'
#     context_object_name = 'bbs'
#
#     def get_queryset(self):
#         return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubric'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
#
#         return context


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    model = Bb
    form_class = BbForm
    success_url = '/detail/{id}'

    # success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {
                'form': bbf
            }
            return render(request, 'bboard/create.html', context=context)
    else:
        bbf = BbForm()
        context = {
            'form': bbf
        }
        return render(request, 'bboard/create.html', context=context)


# class BbAddView(FormView):
#     template_name = 'bboard/create.html'
#     form_class = BbForm
#     initial = {'price': 0.0}
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['rubric'] = Rubric.objects.all()
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def get_form(self, form_class=None):
#         self.object = super().get_form(form_class)
#         return self.object
#
#     def get_success_url(self):
#         return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


def edit(request, pk):
    """
    Редоктирование формы с объявлением
    """
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


class BbEditView(UpdateView):
    """
    Контроллер UpdateView ищет запись по полученным ИЗ URL-параметра ключу или слагу, выводит страницу с формой
    для ее правки, проверяет и сохраняет исправленные данные.
    """
    model = Bb
    form_class = BbForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.get_object().id})


# class BbDeleteView(DeleteView):
#     """
#     Удаление объявления.
#     Контроллер UpdateView ищет запись по полученным ИЗ URL-параметра ключу или слагу, выводит страницу с формой
#     для ее правки, проверяет и сохраняет исправленные данные.
#     """
#     model = Bb
#     success_url = '/'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context


def delete(request, pk):
    """
    Удаление из базы через форму объявлений
    """
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bb.delete()
        return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bb.rubric.pk}))
    else:
        context = {'bb': bb}
        return render(request, 'bboard/bb_confirm_delete.html', context)


class BbIndexView(ArchiveIndexView):
    """
    Контроллер-класс ArchivelndexView выводит хронологический список записей, отсортированных по убыванию значения
    заданного поля.
    """
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'

    # paginate_by = 4

    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field = 'published'
    month_format = '%m'
