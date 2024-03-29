# django-ui-widgets

Add-on for the **django framework** consisting of improved widgets and fields with an expanded viewing interface and advanced features. Django widgets are taken as a basis.

### Package contains:

- [DynamicMultiSelect](#dynamicmultiselect)
- [DynamicSelect](#dynamicselect)
- [DynamicModelField](#dynamicmodelfield)
- [CustomImageField](#customimagefield)
- [AutoUrlInput](#autourlinput)
- [JSONViewWidget](#jsonviewwidget)
- [DateWidget](#datewidget)
- [DivHyperModelForm](#divhypermodelform)


## DynamicMultiSelect

This is a replacement for `SelectMultiple`. In fact, it is an analog of django-autocomplete without using jquery.

Usage example:

```python
from ui.widgets import DynamicMultiSelect

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
In example above `tag_filter` is name of the view url, which consists of filter returning `JsonResponse` object with a list of `dict`s contained `id` and `name` keys:

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

## DynamicSelect

Like `DynamicMultiSelect` *DynamicSelect* is replacement standart `Select` django widget for `ForeignKey` model fields with asynchronius autofillng from specified url. Works without jquery. Using like `DynamicMultiSelect` or through `DynamicModelField` (recomended):

## DynamicModelField

**DynamicModelField** is field using `DynamicSelect` widget. 

The simplest usage example:

```python
form.fields['type'] = DynamicModelField(
    reverse('tag_filter'),
    SkillLabel.objects.filter(id=form.instance.type_id),
    'Field Placeholder',
)
```

In constructor you also can specify `class_name` and optional `attrs` for DynamicSelect widget:

```python
form.fields['type'] = DynamicModelField(
    reverse('tag_filter'),
    SkillLabel.objects.filter(id=form.instance.type_id),
    placeholder='Placeholder',
    class_name='my_class',
    attrs={'style': 'margin-bottom:0'}
)
```
you can use several of these fields on the same page and in the same form

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

**Attention!**
for this widget to work correctly, you must explicitly specify links to media resources in the template after the form, such as: `{{ form.media }}`


## DateWidget

Customized *DateInput* widget:

![alt JSONViewWidget](./doc/time.PNG)

## JSONViewWidget

**JSONViewWidget** - widget for displaying the content of `model.JSONField` (a field officially added in django 3.1). Designed specifically for usage inside admin interface. Usage example:

```python
class SkillAdmin(admin.ModelAdmin):
    formfield_overrides = {
            models.JSONField: {            
                'widget': JSONViewWidget(                
            ) 
        },
    }
```

![alt JSONViewWidget](./doc/json.PNG)

`JSONViewWidget` inspired by [SplitJSONWidget](https://github.com/abbasovalex/django-SplitJSONWidget-form). But it has the following features that are missing in `SplitJSONWidget`, currently:

- adding and removing notes of the tree first level
- editing for array entries of the tree first level
- view, editing and deleting for the notes of embedded levels

# forms


## DivHyperModelForm

custom ModelForm with two new methods:

- **as_ht()** - works like `as_p` in template, but it already contains all the necessary content of the form tag. It means, small calling `{{form.as_p}}` by rendering
deploys to following code:

```html
<form method="post" {{cssclass}}>
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="{{submit}}">
</form>
```

- **as_div** - works like *as_ht*, but instaed of `p` tag to display each item of the form fields it takes `div`

Optional attributes:

- *action* - specify `action` attribute for the `<form>` tag
- *css_class* - specify `class` attribute for the `<form>` tag
- *submit* - specify `value` attribute for `<submit>` tag inside tag form

Usage:

```python
class ProfileUpdateForm(DivHyperModelForm):  

    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super().__init__('submit', 'form_class', *args, **kwargs)
	self.action = reverse('some_next_page')
```
or 
```python
class ProfileUpdateForm(DivHyperModelForm):  
    action = '/'
    submit = 'ok'
    css_class = 'form_class'
    
    class Meta:
        model = Profile
        exclude = ('user',)
```

Create instance and pass to template:

```python
context = {'form': ProfileUpdateForm(submit='ok', request=request)}
render('template_name.html', context, request)
```

in template:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">	
</head>
<body>
	{{form.as_div}}
	{{form.media}}
</body>
```

in above sample usage `{{form.media}}` is optionally like standart form




# Installation:

There are two steps:
- First step: install through *pip* utility from one of the following sources:
    - *pypi*
    ```
    pip install django-ui-widgets
    ```

    - *github* (*latest version*) (*recomended*)
    ```
    pip install git+http://github.com/Sanshain/django-ui-widgets
    ```
- Second step: add **"ui"** app to `INSTALLED_APPS` inside `settings.py` of your project:

   ```py
   INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #...
    
    'ui',
    
    #...
   ]
   ```

Finish




