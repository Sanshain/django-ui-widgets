from django import forms
from django.forms import Widget, MultiWidget, SelectDateWidget
from django.forms.widgets import ChoiceWidget, ClearableFileInput, \
    FileInput, FILE_INPUT_CONTRADICTION, URLInput

f = forms.widgets.CheckboxInput
f = forms.widgets.SelectMultiple
f = forms.widgets.Select


class AutoUrlInput(URLInput):
    class Media:
        # css = {'all': ("iri.css",)}
        js = ("js/auto_url_input.js",)

    template_name = 'forms/widgets/auto_url.html'
    oninput = 'urlFieldPreFill'

    def __init__(self, attrs=None, oninput=None):
        super().__init__(attrs)
        self.attrs['oninput'] = oninput or self.oninput + '(event)'


"""
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
"""


class ImageWidget(FileInput):
    template_name = 'forms/widgets/image_picker.html'

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        if self.is_initial(value):
            return value

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, 'url', False))

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'is_initial': self.is_initial(value),
            'jar_class': '',
            'img_class': '',
            'clr_class': ''
        })
        return context

    # почти дефолтное поведение:

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        return upload

    def use_required_attribute(self, initial):
        return super().use_required_attribute(initial) and not initial

    def value_omitted_from_data(self, data, files, name):
        return (
            super().value_omitted_from_data(data, files, name)
        )


class DynamicMultiSelect(ChoiceWidget):  # ChoiceWidget

    duty_symbols = {
        '+': 'plus',
        '#': 'sharp'
    }

    template_name = 'forms/widgets/dynamic_multi_select.html'

    # ChoiceWidget:
    # allow_multiple_selected = True
    # optgroups = ChoiceWidget.optgroups
    # create_option = ChoiceWidget.create_option
    #
    # format_value = ChoiceWidget.format_value  # форматирует вывод. Исп в Widget
    #
    # subwidgets = ChoiceWidget.subwidgets
    # options = ChoiceWidget.options
    #
    # __deepcopy__ = ChoiceWidget.__deepcopy__
    # id_for_label = ChoiceWidget.id_for_label

    def __init__(self, url='', placeholder=None, attrs=None, **kwargs):  # choices=(), # # ChoiceWidget
        if placeholder:
            attrs = attrs or {}
            attrs['placeholder'] = placeholder
        super().__init__(attrs, **kwargs)
        self.url = url
        # self.choices = choices  # ChoiceWidget

    def get_context(self, name, value, attrs):

        # from django.forms.models import ModelChoiceIterator
        # ModelChoiceIterator

        def_attrs = ['id', 'required', 'multiple']  # multiple todo in template
        default_attrs = {key: attrs.pop(key) for key in def_attrs if key in attrs}

        context = super().get_context(name, value, attrs)
        # ChoiceWidget:
        # context['widget']['optgroups'] = self.optgroups(name, context['widget']['value'], attrs)

        context['widget']['url'] = self.url
        context['default_attrs'] = default_attrs
        return context

    def value_from_datadict(self, data, files, name):
        return data.getlist(name)

    def create_option(self, name, value, label, *args, **kwargs):
        options = super().create_option(name, value, label, *args, **kwargs)
        options['attrs'].update({
            'data-id': value,
            'data-hint': label,
            'selected': True,

            'in_swarm_id': name + '_tag_' + self.valid_id_format(label),
        })
        return options

    # not inheritance:
    def valid_id_format(self, name: str):
        for char in self.duty_symbols:
            name = name.replace(char, self.duty_symbols[char])
        return name
