# -*- coding: utf-8 -*-
import datetime
# from distutils.version import StrictVersion


from django import get_version, forms
from django.forms import Widget
from django import utils

from django.forms.utils import flatatt

import json  # # import simplejson as json
import copy


class JSONViewWidget(forms.Widget):
    # class Media:
    #     # css = {'all': ("iri.css",)}
    #     js = ("js/auto_url_input.js",)

    label_def_style = 'style="display: inline-block;float:none;"'
    input_def_style = 'style="width:50vw;"'

    def __init__(self, attrs=None, newline='<br/>\n', sep='__', debug=False):
        self.newline = newline
        self.separator = sep
        self.debug = debug
        Widget.__init__(self, attrs)

    def _label_render(self, attrs, key):
        return f"""<label {self.label_def_style} for="{attrs['id']}">{key}:</label>"""

    def _delete_btn(self, key):
        btn = f"""<div class='del_key' onclick='del_key(event, "{key}")'></div>"""
        return btn

    def _append_value(self):
        btn = f"""<div class='append_value' onclick='append_value(event)'></div>"""
        return btn

    def _as_text_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "type": 'text',
            "name": "%s%s%s" % (name, self.separator, key),
        })
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        input_def_style = self.input_def_style[:-1] + 'margin-left:-3px;"'
        return f"""
                <label {self.label_def_style} for="{attrs['id']}">{key}:</label>
                <input{flatatt(attrs)}  {input_def_style} />
                {self._delete_btn(attrs['id'])}"""

    def _as_textarea_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "name": "%s%s%s" % (name, self.separator, key),
        })
        attrs['id'] = attrs.get('name', None)
        return f"""
            <label for="{attrs['id']}">{key}:</label>
            <textarea{flatatt(attrs)} {self.input_def_style} rows=10>{utils.encoding.force_text(value)}
            </textarea>
        """

    def _as_number_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "type": 'number',
            "name": "%s%s%s" % (name, self.separator, key),
        })
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        return f"""<label  {self.label_def_style} for="{attrs['id']}">{key}:</label><input{flatatt(attrs)} />"""

    def _as_float_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "type": 'number',
            "step": '0.01',
            "name": "%s%s%s" % (name, self.separator, key),
        })
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        return f"""
            <label for="{attrs['id']}">{key}:</label>
            <input{flatatt(attrs)} />
        """

    def _as_date_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "type": 'date',
            "name": "%s%s%s" % (name, self.separator, key),
        })
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        return f"""
            <label for="{attrs['id']}">{key}:</label>
            <input{flatatt(attrs)} />
        """

    def _as_datetime_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "type": 'datetime-local',
            "name": "%s%s%s" % (name, self.separator, key),
        })
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        return f"""
            <label for="{attrs['id']}">{key}:</label>
            <input{flatatt(attrs)} />
        """

    def _as_checkbox_field(self, name, key, value, is_sub=False):
        classes = self.attrs['class']
        classes = [c for c in classes.split() if c != 'form-control']
        classes.append("switch")
        attrs = self.build_attrs(self.attrs, {
            "type": 'checkbox',
            "class": " ".join(classes),
            "onclick": "this.previousSibling.value=!JSON.parse(this.previousSibling.value)",
        })
        hidden_name = "%s%s%s" % (name, self.separator, key)
        attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        checked = '' if not bool(value) else 'checked'
        return f"""
            <label {self.label_def_style} for="{attrs['id']}">{key}:</label>
            <input type="hidden" name="{hidden_name}" value="{attrs['value'].lower()}"><input{flatatt(attrs)} {checked}/>
        """

    def _as_select_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, {
            "size": "none",
            "name": "%s%s%s" % (name, self.separator, key),
        })
        # attrs['value'] = utils.encoding.force_text(value)
        attrs['id'] = attrs.get('name', None)
        # attrs['disabled'] = True
        attrs.pop('name', None)  # todo (make readonly until todo valid multiple params come in)

        label = f"""<label for="{attrs['id']}">{key}:</label>"""

        options = ''
        for option in value:
            options += f'<option selected value="{option}">{option}</option>'

        input_def_style = self.input_def_style[:-1] + 'margin-top: 3px;"'
        return f"""
                {label}<select{flatatt(attrs)} class='jsn_array' multiple 
                {input_def_style}>{options}</select>
                {self._delete_btn(attrs['id'])}
                {self._append_value()}"""

    def _to_build(self, name, json_obj):
        """
        Генерирует дерево инпутов
        :param name:
        :param json_obj: объект json
        :return:
        """
        inputs = []
        if isinstance(json_obj, list):
            if all(isinstance(item, (str, int, float, bool)) for item in json_obj):
                name, _, key = name.rpartition(self.separator)
                inputs.append(self._as_select_field(name, key, json_obj))
            else:
                title = name.rpartition(self.separator)[2]
                _l = []  # ['%s:%s' % (title, self.newline)]
                for key, value in enumerate(json_obj):
                    _l.append(self._to_build("%s%s%s" % (name, self.separator, key), value))
                inputs.extend([_l])
        elif isinstance(json_obj, dict):
            title = name.rpartition(self.separator)[2]
            _l = []  # ['%s:%s' % (title, self.newline)]
            # inputs.extend('<div>Заголовок</div>')
            for key, value in json_obj.items():
                if value != {}:
                    _l.append(self._to_build("%s%s%s" % (name, self.separator, key), value))
            inputs.extend([_l])
        elif isinstance(json_obj, str):
            name, _, key = name.rpartition(self.separator)
            if len(json_obj) > 50:
                inputs.append(self._as_textarea_field(name, key, json_obj))
            else:
                inputs.append(self._as_text_field(name, key, json_obj))
        elif isinstance(json_obj, bool):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_checkbox_field(name, key, json_obj))
        elif isinstance(json_obj, int):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_number_field(name, key, json_obj))
        elif isinstance(json_obj, float):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_float_field(name, key, json_obj))
        elif isinstance(json_obj, datetime.date):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_date_field(name, key, json_obj))
        elif isinstance(json_obj, datetime.datetime):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_datetime_field(name, key, json_obj))
        elif json_obj is None:
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, ''))
        return inputs if len(inputs) > 1 else inputs[0]

    def _prepare_as_div(self, input_list, level):
        """
        Форматирование дерева инпутов
        :param input_list:
        :param level:
        :return:
        """
        form_group_class = ''
        input_list = [input_list] if type(input_list) is str else input_list
        if input_list:
            result = ''
            for item in input_list:
                class_ex = ''
                if level == 0 or level == 1:
                    class_ex = 'nested'

                if isinstance(item, list) and len(input_list) == 1:
                    result += '%s' % self._prepare_as_div(item, level)
                elif isinstance(item, list):
                    if level == 0:
                        result += f'<div class="{form_group_class} {class_ex}">'
                        result += '%s' % self._prepare_as_div(item, level + 1)
                        result += '</div>'
                    else:
                        result += f'<div class="{form_group_class} {class_ex}">'
                        result += '%s' % self._prepare_as_div(item, level + 1)
                        result += '</div>'
                else:
                    if level == 1:
                        level_title = ''  # '<p>hhhhhhh</p>'
                        result += '%s<div class="%s col-md-12">%s</div>' % (level_title, form_group_class, item)
                    else:
                        result += '<div class="%s">%s</div>' % (form_group_class, item)
            return result
        return ''

    def _to_pack_up(self, root_node, raw_data):

        copy_raw_data = copy.deepcopy(raw_data)
        result = []

        def _to_parse_key(k, v):
            if k.find(self.separator) != -1:
                apx, _, nk = k.rpartition(self.separator)
                if apx.startswith('__'):
                    apx = apx[2:]

                try:
                    # parse list
                    int(nk)
                    l = []
                    obj = {}
                    index = None
                    if apx != root_node:
                        for key, val in list(copy_raw_data.items()):
                            head, _, t = key.rpartition(self.separator)
                            _, _, index = head.rpartition(self.separator)
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                try:
                                    int(t)
                                    l.append(val)
                                except ValueError:
                                    if index in obj:
                                        obj[index].update({t: val})
                                    else:
                                        obj[index] = {t: val}
                                del copy_raw_data[key]
                        if obj:
                            for i in obj:
                                l.append(obj[i])
                    l.append(v)
                    return _to_parse_key(apx, l)
                except ValueError:
                    # parse dict
                    d = {}
                    if apx != root_node:
                        for key, val in list(copy_raw_data.items()):
                            _, _, t = key.rpartition(self.separator)
                            try:
                                int(t)
                                continue
                            except ValueError:
                                pass
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                d.update({t: val})
                                del copy_raw_data[key]
                    v = {nk: v}
                    if d:
                        v.update(d)
                    return _to_parse_key(apx, v)
            else:
                return v

        for k, v in list(raw_data.items()):
            if k in copy_raw_data:
                # to transform value from list to string
                v = v[0] if isinstance(v, list) and len(v) is 1 else v
                if k.find(self.separator) != -1:
                    d = _to_parse_key(k, v)
                    # set type result
                    if not len(result):
                        result = type(d)()
                    try:
                        result.extend(d)
                    except:
                        result.update(d)
        return result

    def value_from_datadict(self, data, files, name):
        """
        распаковка для валидации
        :param data:
        :param files:
        :param name:
        :return:
        """
        data_copy = copy.deepcopy(data)
        result = self._to_pack_up(name, data_copy)
        return json.dumps(result)

    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = json.loads(value)
        except (TypeError, KeyError):
            pass
        inputs = self._to_build(name, value or {})
        result = self._prepare_as_div(inputs, 0)

        append_btn = f'<div class="append_btn" onclick="add_json_field(event)"></div>'
        result = f'<div class="json_container" style="float:left" class="row">{result}{append_btn}</div>'

        # add_json_field        '

        if self.debug:
            # render json as well
            source_data = u'<hr/>Source data: <br/>%s<hr/>' % str(value)
            result = '%s%s' % (result, source_data)
        return utils.safestring.mark_safe(result)

    # template_name =
    #
    # def render(self, name, value, attrs=None, renderer=None):
    #     """Render the widget as an HTML string."""
    #     context = self.get_context(name, value, attrs)
    #     return self._render(self.template_name, context, renderer)

    class Media:
        css = {'all': ("style/json_field.css",)}
        js = ("js/json_field.js",)
