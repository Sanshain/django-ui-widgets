from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import BoundField, ImageField, MultipleChoiceField, ModelChoiceField, Form, ModelForm

from django.forms import ModelMultipleChoiceField

from django_extension.widgets import DynamicMultiSelect, ImageWidget, DynamicSelect


class DynamicBoundField(BoundField):

    def __init__(self, form: ModelForm, field, name):
        if not isinstance(form, ModelForm):
            raise Exception('Use `DynamicSelect` field just for ModelForm instances')
        if not form.instance:
            field.queryset = field.queryset.none()

        super().__init__(form, field, name)


class ViewImageField(BoundField):

    def __init__(self, form, field, name, css_class='upload', back_image=None):
        self.attrs = None
        self.back_image = back_image
        self.css_class = css_class

        super(ViewImageField, self).__init__(form, field, name)

    def label_tag(self, contents=None, attrs: dict or None = None, label_suffix=None):
        self.attrs = attrs or {}
        self.set_attr('class', self.css_class) \
            .set_attr('style', 'background-image:url({});'.format(self.back_image)) \
            .set_attr('style', 'color:{}'.format('transparent' if self.back_image else None))
        return super().label_tag(contents, self.attrs, label_suffix)

    def set_attr(self, attr, value):
        if value:
            if attr in self.attrs:
                self.attrs[attr] += value
            else:
                self.attrs[attr] = value
        return self


class CustomImageField(ImageField):
    """
    отвечает за представление поля в шаблоне через методы класса BoundField, т.к.
    BoundField - отвечает за представление поля в шаблоне
    Нам надо переопределить label_tag, поэтому возвращаем свой класс BoundField с переопределенным методом label_tag
    """
    widget = ImageWidget

    def __init__(self, *, label_css_class: str = 'upload', back_image=None, onchange='upload_photo', **kwargs):
        """
        :param label_css_class: класс для лэйбла
        :param kwargs:
        :param onchange: имя соьытия обработки
        """
        hint = kwargs.pop('hint', None)
        super().__init__(**kwargs)
        if onchange:
            self.widget.attrs['onchange'] = f'{onchange}(event)'

        self.label_css_class = label_css_class
        self.back_image = (settings.STATIC_URL + 'images/' + back_image) if back_image else None
        # self.widget.attrs['style'] = 'visibility:hidden'
        self.widget.attrs['style'] = 'width:0;height:0;padding:0;'
        self.widget.default_image = back_image
        self.widget.hint = hint


class DynamicModelField(ModelChoiceField):
    """
    alpha
    """
    widget = DynamicSelect

    # get_bound_field = lambda self, form, field_name: DynamicBoundField(form, self, field_name)

    def __init__(self, url, queryset, placeholder='', class_name=None, attrs=None, **kwargs):
        kwargs['required'] = kwargs.get('required', False)
        super().__init__(queryset, widget=self.widget(url, attrs=attrs), empty_label='', **kwargs)
        self.widget.attrs['placeholder'] = placeholder
        if class_name:
            self.widget.attrs['class'] = class_name

    def get_bound_field(self, form, field_name):
        return DynamicBoundField(form, self, field_name)

    # def to_python(self, value):
    #     if value in self.empty_values:
    #         return None
    #     try:
    #         key = self.to_field_name or 'pk'
    #         if isinstance(value, self.queryset.model):
    #             value = getattr(value, key)
    #         value = self.queryset.get(**{key: value[0]})
    #     except (ValueError, TypeError, self.queryset.model.DoesNotExist):
    #         raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
    #     return value


class DynamicChoiceField(ModelMultipleChoiceField):
    """
    alpha
    """

    widget = DynamicMultiSelect
    """
    check_queryset - queryset для проверки внутри _check_values
    """

    def __init__(self, queryset, url='/', check_queryset=None, class_name=None, **kwargs):
        super().__init__(queryset, widget=self.widget(url), **kwargs)
        self.check_queryset = check_queryset
        if class_name:
            self.widget.attrs['class'] = class_name

    def _check_values(self, value):
        """
        Given a list of possible PK values, return a QuerySet of the
        corresponding objects. Raise a ValidationError if a given value is
        invalid (not a valid PK, not in the queryset, etc.)
        """
        key = self.to_field_name or 'pk'
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            value = frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages['list'],
                code='list',
            )
        # можно оптимизировать:
        for pk in value:
            try:
                self.queryset.filter(**{key: pk})
            except (ValueError, TypeError):
                raise ValidationError(
                    self.error_messages['invalid_pk_value'],
                    code='invalid_pk_value',
                    params={'pk': pk},
                )

        qs = (self.check_queryset or self.queryset.model.objects.all()).filter(**{'%s__in' % key: value})
        pks = {str(getattr(o, key)) for o in qs}
        for val in value:
            if str(val) not in pks:
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )
        return qs
