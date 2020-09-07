from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_extension.forms import HmlModelForm


class DivMixinForm:                                                        # (HmlModelForm)
    """
    Делает help_text_html невидимым и добавляет к нему класс help-text
    а так же скрывает реализацию самой формы
    """

    def as_div(self):

        as_p = self._html_output(
            normal_row=u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row=u'<div class="error">%s</div>',
            row_ender='</div>',
            help_text_html=u'<div hidden class="help-text">%s</div>',
            errors_on_separate_row=False)

        csrf_t = '<p style="color:red">Set csrf in your view</p>'
        submit = self.submit
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''

        if self.request != None:
            csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'
        if self.submit == 'def':
            submit = 'in_' + self.__class__.__name__ + '_notdefined'

        html = '<form method="post" ' + cssclass + '>' + csrf_t + as_p + '<input type="submit" value=' + submit + '></form>'

        return mark_safe(html)



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