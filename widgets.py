from django import forms
from django.forms import Widget, MultiWidget, SelectDateWidget

f = forms.widgets.CheckboxInput
f = forms.widgets.SelectMultiple
f = forms.widgets.Select


class ToggleWidget(Widget):
    template_name = 'django/forms/widgets/checkbox.html'
    option_template_name = 'django/forms/widgets/checkbox.html'

    class Media:
        css = {'all': ("",)}
        js = ("",)

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}

        default_options = {
            'toggle': 'toggle',
            'offstyle': 'danger'
        }
        options = kwargs.get('options', {})
        default_options.update(options)
        for key, val in default_options.items():
            attrs['data-' + key] = val

        super().__init__(attrs)


class DynamicMultiSelect(Widget):
    def __init__(self, url='', attrs=None):

        super().__init__(attrs)
        self.url = url

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['url'] = self.url
        return context
