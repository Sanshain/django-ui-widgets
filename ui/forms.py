from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import NON_FIELD_ERRORS

# для кастомного Field:
from django.forms import BoundField, Field, ImageField, ModelForm, FileField
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, conditional_escape
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

from django.middleware.csrf import get_token


class HyperModelForm(ModelForm):
    action = ''

    def __init__(self, *args, submit='def', cssclass='', **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)        
        self.submit = submit
        self.css_class = cssclass

    def as_ht(self):

        csrf_t = 'None'
        submit = self.submit
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''

        if self.request != None:
            csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'
        if self.submit == 'def':
            submit = 'in_' + self.__class__.__name__ + '_not_defined'

        html = '<form method="post" ' + cssclass + '>' + csrf_t + self.as_p() + '<input type="submit" value=' + submit + '></form>'

        return mark_safe(html)

    def __unicode__(self):
        return self.as_h()


class DivHyperModelForm(HyperModelForm):  # (HmlModelForm)
    """
    Делает help_text_html невидимым и добавляет к нему класс help-text
    а так же скрывает реализацию самой формы
    """

    def as_div(self):

        _multi_type = any(isinstance(field, FileField) for field in self.fields.values())

        enctype = "enctype=\"multipart/form-data\"" if _multi_type else ''
        action = self.action
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''

        as_p = self._html_output(
            normal_row=u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row=u'<div class="error">%s</div>',
            row_ender='</div>',
            help_text_html=u'<div hidden class="help-text">%s</div>',
            errors_on_separate_row=False)
        csrf_t = '<p style="color:red">Set csrf in your view</p>' if self.request == None \
            else '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'
        submit = 'in_' + self.__class__.__name__ + '_notdefined' if self.submit == 'def' \
            else self.submit

        html = f'<form method="post" {cssclass} {action} {enctype}> ' \
               f'   {csrf_t} {as_p} <input type="submit" value="{submit}">' \
               f'</form>'

        return mark_safe(html)


# example:

"""
class CreatePerson(HyperModelForm):
    # required_css_class = 'required_fields'
    error_css_class = 'error_class'  # работает, но не востребовано

    class Meta(object):
        model = Profile
        fields = (
            'username', 'password', 'first_name', 'last_name', 'email', 'City', 'Sex', 'Age', 'Image')  # exclude
        # exclude = ('username',)
        labels = {
            'username': 'Введите желаемый логин',
            'password': 'Пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия либо Отчество',
            'email': 'Почта',
            'Image': 'Изображение',
        }
        help_texts = {
            'username': (''),
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': u'Пароль'}),
            'email': forms.EmailInput(attrs={'placeholder': 'mail@example.ru'}),
            'Image': forms.FileInput(
                attrs={
                    'accept': "image/jpeg,image/png",
                    'style': 'visibility:hidden',
                    'onchange': 'file_upload(this, event)'}),  # 'style':  display:none
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
                # если нужны будут два уникальных поля
            },
            'username': {
                'unique': u"Пользователь с таким именем уже существует",
            },
        }

    def __init__(self, *args, **kwargs):
        super(CreatePerson, self).__init__(*args, **kwargs)
        self.submit = u'Присоединиться'
        self.css_class = ''

        self.fields['email'].validators = [EmailValidator(message="Некорректный адрес электронной почты")]
        self.fields['Image'] = CustomImageField(self.fields['Image'])
"""
