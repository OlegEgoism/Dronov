import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.dates import ArchiveIndexView, YearMixin, MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .forms import BbForm, UserLoginForm, SearchForm, ImgForm, EmailForm
from .models import Bb, Rubric, Img
from .serializers import RubricSerializer


def index(request):
    """
    Главная страница
    """
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


def rubrics(request):
    """
    Редактор рубрик в форме
    """
    RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_delete=True)
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = RubricFormSet()
    context = {
        'formset': formset
    }
    return render(request, 'bboard/rubrics.html', context)
    # return {'rubric': Rubric.objects.all()}


def bbs(request, rubric_id):
    """
    Обработка встроенных набров форм
    """
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)


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


class BbCreateView(SuccessMessageMixin, CreateView):
    template_name = 'bboard/create.html'
    model = Bb
    form_class = BbForm
    success_url = '/detail/{id}'
    success_message = 'Объявление о продаже товара "%(title)s" создано.'

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
            messages.add_message(request, messages.SUCCESS, 'Объявление исправлено', extra_tags='first second')
            # first_message_text = messages[0].message
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
    """
    Дата в html
    """
    model = Bb
    date_field = 'published'
    month_format = '%m'


# def get_login(request):
#     """
#     Вход на сайт
#     """
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserLoginForm
#     context = {
#         'form': form
#     }
#     return render(request, 'registration/login.html', context=context)
#
# def get_logout(request):
#     """
#     Выход с сайта
#     """
#     logout(request)
#     return redirect('login')


class Login(LoginView):
    """
    Вход на сайт
    """
    authentication_form = UserLoginForm
    template_name = 'registration/login.html'
    next = 'registration/login.html'


class Logout(LogoutView):
    """
    Выход с сайта
    """
    template_name = 'registration/logout.html'


class SLPasswordResetView(PasswordResetView, SuccessMessageMixin, LoginRequiredMixin):
    template_name = 'registration/password_reset.html'
    subject_template_name = 'registration/reset_subject.txt'
    email_template_name = 'registration/reset_email.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = 'Пароль пользователя сброшен'


def search(request):
    """Поиск"""
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            # rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bb.objects.filter(title__icontains=keyword)
            context = {'bbs': bbs}
            return render(request, 'bboard/search_result.html', context=context)  # Куда перейдем после поиска
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context=context)  # Форма поиска


def formset_processing(request):
    FS = formset_factory(SearchForm, extra=3, can_order=True, can_delete=True)
    if request.method == 'POST':
        formset = FS(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    keyword = form.cleaned_data['keyword']
                    # rubric_id = form.cleaned_data['ORDER']
                    bbs = Bb.objects.filter(title__icontains=keyword)
                    context = {'bbs': bbs}
                    return render(request, 'bboard/process_result.html', context=context)
    else:
        formset = FS()
    context = {'formset': formset}
    return render(request, 'bboard/formset.html', context=context)


def imgadd(request):
    """Добавление фото через форму"""
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('img'):
                img = Img()
                img.desc = form.cleaned_data['desc']
                img.img = file
                img.save()
            return redirect('index')
    else:
        form = ImgForm()
        context = {'form': form}
    return render(request, 'bboard/imgadd.html', context=context)


def delete_img(request, pk):
    """
    Удаление записи и отдельно удаляется картинка.
    """
    img = Img.objects.get(pk=pk)
    img.img.delete()
    img.delete()
    return redirect('index')


def get_email(request):
    """
    Отправка электронных писем
    """
    if request.method == 'POST':
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            mail = send_mail(emailform.cleaned_data['subject'], emailform.cleaned_data['content'], '',
                             recipient_list=('olegpustovalov220@gmail.com',), fail_silently=True)
            if mail:
                context = {
                    'title': 'Обратная связь',
                    'emailform': emailform
                }
                return render(request, 'bboard/mail.html', context=context)
            else:
                context = {
                    'title': 'Письмо отправлено',
                    'emailform': emailform
                }
                return render(request, 'bboard/mail.html', context=context)
    else:
        emailform = EmailForm()
    context = {
        'title': 'Ошибка отправки письма',
        'emailform': emailform
    }
    return render(request, 'bboard/mail.html', context=context)


@api_view(['GET', 'POST'])
def api_rubrics(request):
    """
    Второй принцип REST: идент.ификация действия по НТТР-методу
    """
    if request.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_rubric_detail(request, pk):
    rubric = Rubric.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = RubricSerializer(rubrics)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = RubricSerializer(rubric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rubric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIRubrics(APIView):
    def get(self, request):
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIRubric(generics.ListCreateAPIView):
    """
    Контроллер-класс низкого уровня
    """
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIRubricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIRubricList(generics.ListAPIView):
    """Список рубрик"""
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIRubricViewSet(ModelViewSet):
    """Метаконтроллеры (для добавления новой рубрики .../rubset/)"""
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = (IsAuthenticated,)


class APIRubricViewSetRe(ReadOnlyModelViewSet):
    """Пример метаконтроллера, реализующего только считывание данных"""
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
