from django.forms import DateInput, TimeInput


class DateWidget(DateInput):
    template_name = 'forms/widgets/date.html'

    def __init__(self, placeholder='', attrs=None, format=None):
        # attrs['type'] = 'date'
        super().__init__(attrs, format)
        self.placeholder = placeholder

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = 'date'  # self.input_type
        context['placeholder'] = self.placeholder or 'Введите дату'
        return context


class TimeWidget(TimeInput):
    template_name = 'forms/widgets/time.html'
