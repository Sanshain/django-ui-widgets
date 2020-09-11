# django-ui-widgets

This is a plugin for django consisting of improved widgets and fields with a relevant view interface and advanced features based on some django widgets. Some of them:

## DynamicMultiSelect

This is a replacement for `SelectMultiple`. In fact, it is an analog of django-autocomplete without using jquery. Usage:

```python
class ProfileUpdateForm(ModelForm): 

    labels = ModelMultipleChoiceField(
        queryset=SkillLabel.objects.all(),
        widget=DynamicMultiSelect(reverse_lazy('tag_filter'))
    )

    class Meta:
        model = Profile

    def __init__(self, *args, **kwargs):

        super().__init__('submit', *args, **kwargs)
        if 'data' not in kwargs:
            self.fields['labels'].queryset = SkillLabel.objects.filter(profile=self.instance)
            self.fields['labels'].widget.choices = ModelChoiceIterator(self.fields['labels'])
```
In the example above, `tag_filter` is a name of view url, that consists of filter returning `JsonResponse` object with a list of `dict`s contained `id` and `name` keys:

```python
def tag_filter(request: HttpRequest):

    pattern = request.GET.get('query', '')
    result = SkillLabel.objects\
        .filter(name__startswith=pattern)\
        .extra(select={'hint': 'name'}) \
        .values('id', 'name') if pattern else ()

    return JsonResponse(list(result), safe=False)
```
You can also use `.annotate(value=F('name')` instead of `extra` for receiving proper name `name` for view in template.

Also pay attention to the choice assignment when transmitting data. This is necessary for correct form validation when checking primary keys

## CustomImageField

A field that hides input with the file type and allows you to set the css class for the label pointing to it. 
This is a common (and almost default) practice of decorating 'input[type=file]' in classic frontend development, which requires a lot of actions. 
With this component, you can do it in one line. Recommended usage:

```python
    image = CustomImageField(label_css_class='image_icon', back_image='photo_up.jpg')
```

In above sample by default inside CustomImageField is used `ImageWidget`. You can override this widget if you want. 
However, this is not recommended, since in this case you will need to manually implement the display of the image when it is updated

## AutoUrlInput

Replacement for URLInput. Adds an automatic 'https://' extension at the beginning of the line if the address is invalid

