from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm, DecimalField
from django.forms.widgets import Select

from .models import Bb, Rubric, Img


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = '__all__'  # 'rubric', 'kind', 'title', 'content', 'price'

# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric', 'kind')
#         labels = {'title': 'Название товара'}
#         help_texts = {'rubric': 'Не забудьте выбрать рубрику', 'kind': 'Выберите одну позицию'}
#         field_classes = {'price': DecimalField}
#         widgets = {'rubric': Select(attrs={'size': 6}), 'kind': Select(attrs={'size': 4})}


class BbForm(forms.ModelForm):
    content = forms.CharField(label='Описание', label_suffix='(для сайта)', initial='Нет описания',
                              widget=forms.widgets.Textarea)
    price = forms.DecimalField(label='Цена товара', max_digits=6, decimal_places=2,
                               error_messages={'validate_even': 'Неправельные данные'}, initial=0)
    rubric = forms.ModelChoiceField(label='Рубрика', queryset=Rubric.objects.all(), help_text='Не забудьте выбрать',
                                    widget=forms.widgets.Select(attrs={'size': 0}))
    kind = forms.Select()
    captcha = CaptchaField(label='Введите текст', error_messages={'invalid': 'Не верно'})

    class Meta:
        model = Bb
        fields = 'title', 'content', 'price', 'rubric', 'kind'
        labels = {'title': 'Название товара'}


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class SearchForm(forms.Form):
    keyword = forms.CharField(label='Искомое слово', max_length=20)
    # rubric = forms.ModelChoiceField(label='Рубрика', queryset=Rubric.objects.all())
    error_css_class = 'error'
    required_css_class = 'required'


class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение',
                           validators=[validators.FileExtensionValidator(allowed_extensions=('gif', 'jpg', 'png'))],
                           error_messages={'invalid_extension': 'Этот формат файлов не поддерживается'},
                           widget=forms.widgets.ClearableFileInput(attrs={'multiple': True}))  # Позволяет загружать сразу несколько файлов.
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())


    class Meta:
        model = Img
        fields = '__all__'


class EmailForm(forms.Form):
    subject = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'style': 'margin:10px; padding:10px; height:40px', 'class': 'form-control col-sm-8', 'placeholder': 'Напишите вашу почту'}))
    content = forms.CharField(label='Текст письма', widget=forms.Textarea(attrs={'style': 'margin:10px; padding:10px; height:200px', 'class': 'form-control col-sm-8', 'placeholder': 'Напишите текст письма'}))
