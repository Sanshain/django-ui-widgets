from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.middleware.csrf import get_token
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_extension.forms import HyperModelForm


class HyperFormMixin:

    def __init__(self, submit='def', cssclass='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.submit = submit
        self.css_class = cssclass

    def as_ht(self):

        csrf_t = 'None'
        submit = self.submit
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''

        if self.request != None:
            csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'
        if self.submit == 'def':
            submit = 'in_' + self.__class__.__name__ + '_notdefined'

        html = '<form method="post" ' + cssclass + '>' + csrf_t + self.as_p() + '<input type="submit" value=' + submit + '></form>'

        return mark_safe(html)

    def __unicode__(self):
        return self.as_h()


"""
class SignUpForm(UserCreationForm, DivMixinForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Profile
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.submit = u'Присоединиться'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
"""
