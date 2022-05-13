from django.forms.forms import Form
from django.forms import ModelForm, CharField
from tinymce import TinyMCE
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Field, Button, Submit

from .models import Page, BilingualPage


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PageForm(ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'site', 'category', 'order', 'content']
        labels = {
            'title': 'Tytuł',
            'content': 'Treść',
            'category' : 'Kategoria',
            'order' : 'Kolejność',
            'site' : 'Strona'
        }

    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.include_media = True
        self.fields['content'] = CharField( widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        ))

        layout = []
        layout.append('title')
        layout.append('site')
        layout.append('category')
        layout.append('order')
        layout.append('content')
        layout.append(FormActions(
            Submit('submit', 'Zapisz'),
            Submit('delete', 'Usuń'),
            css_class='text-right',
        ))
        self.helper.layout = Layout(*layout)

class BilingualPageForm(ModelForm):
    class Meta:
        model = BilingualPage
        fields = ['title', 'title_polish', 'category', 'order', 'content', 'content_polish']
        labels = {
            'title': 'Tytuł (Angielski)',
            'title_polish': 'Tytuł (Polski)',
            'content': 'Treść (Angielski)',
            'content_polish': 'Treść (Polski)',
            'category' : 'Kategoria',
            'order' : 'Kolejność',
        }

    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.include_media = True
        self.fields['content'] = CharField( widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        ))
        self.fields['content_polish'] = CharField( widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        ))

        layout = []
        layout.append('title')
        layout.append('title_polish')
        layout.append('category')
        layout.append('order')
        layout.append('content')
        layout.append('content_polish')
        layout.append(FormActions(
            Submit('submit', 'Zapisz'),
            Submit('delete', 'Usuń'),
            css_class='text-right',
        ))
        self.helper.layout = Layout(*layout)