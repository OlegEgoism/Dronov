from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, DecimalField
from django.forms.widgets import Select

from .models import Bb, Rubric


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

    class Meta:
        model = Bb
        fields = 'title', 'content', 'price', 'rubric', 'kind'
        labels = {'title': 'Название товара'}


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
