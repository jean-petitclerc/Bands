from django import forms
from django.forms import Form, ModelForm, Textarea
from .models import Band, Genre


class FormAjoutGenre(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['genre_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre_desc'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Genre
        fields = ['genre_name','genre_desc']
        labels = {'genre_name': ('Nom'), 'genre_desc': ('Description')}
        widgets = {
            'genre_desc': Textarea(attrs={'rows': 8}),
        }

        def clean_genre_desc(self):
            return self.cleaned_data['genre_desc'] or None


class FormModifGenre(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['genre_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre_desc'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Genre
        fields = ['genre_name','genre_desc']
        labels = {'genre_name': ('Nom'), 'genre_desc': ('Description')}
        widgets = {
            'genre_desc': Textarea(attrs={'rows': 8}),
        }

        def clean_genre_desc(self):
            return self.cleaned_data['genre_desc'] or None


class FormAjoutBand(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['band_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['band_desc'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Band
        fields = ['band_name','band_desc']
        labels = {'band_name': ('Nom'), 'band_desc': ('Description')}
        widgets = {
            'band_desc': Textarea(attrs={'rows': 8}),
        }

        def clean_band_desc(self):
            return self.cleaned_data['band_desc'] or None


class FormModifBand(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['band_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['band_desc'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Band
        fields = ['band_name','band_desc']
        labels = {'band_name': ('Nom'), 'band_desc': ('Description')}
        widgets = {
            'band_desc': Textarea(attrs={'rows': 8}),
        }

        def clean_band_desc(self):
            return self.cleaned_data['band_desc'] or None


class FormConfirmation(Form):
    dummy = forms.CharField()
