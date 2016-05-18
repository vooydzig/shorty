from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(required=True, widget=forms.TextInput(attrs={'placeholder': 'URL goes here...'}))
