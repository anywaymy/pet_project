from django import forms

from main.models import SendMessage


class SendMessageForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your name or it will be taken from your profile',
        'id': 'name'
    }), required=False)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'id': 'email'
    }))

    textarea = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your message',
        'id': 'message'
    }))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('name') and (not self.user or not self.user.is_authenticated):
            self.add_error('name', 'Поле "name" обязательно, если не авторизованы')
        return cleaned_data

    class Meta:
        model = SendMessage
        fields = ('name', 'email', 'textarea',)
