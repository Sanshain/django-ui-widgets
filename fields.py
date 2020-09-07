from django.forms import BoundField, ImageField, MultipleChoiceField

from django.forms import ModelMultipleChoiceField


class ViewImageField(BoundField):

    def __init__(self, form, field, name, css_class='upload'):
        self.css_class = css_class
        super(ViewImageField, self).__init__(form, field, name)

    def label_tag(self, contents=None, attrs: dict or None = None, label_suffix=None):
        attrs = attrs or {}
        if 'class' in attrs:
            attrs['class'] += self.css_class
        else:
            attrs['class'] = self.css_class
        return super().label_tag(contents, attrs, label_suffix)


class CustomImageField(ImageField):
    """
    отвечает за представление поля в шаблоне через методы класса BoundField, т.к.
    BoundField - отвечает за представление поля в шаблоне
    Нам надо переопределить label_tag, поэтому возвращаем свой класс BoundField с переопределенным методом label_tag
    """

    def get_bound_field(self, form, field_name):
        return ViewImageField(form, self, field_name, css_class=self.label_css_class)

    def __init__(self, *, label_css_class: str = 'upload', **kwargs):
        """

        :param label_css_class: класс для лэйбла
        :param kwargs:
        """
        super(CustomImageField, self).__init__(**kwargs)
        self.label_css_class = label_css_class
        self.widget.attrs['style'] = 'visibility:hidden'




class DynamicChoiceField(MultipleChoiceField):

    def __init__(self, *args, class_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        if class_name:
            self.widget.attrs['class'] = class_name
        s = self

