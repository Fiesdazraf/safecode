from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'message': 'پیام شما',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام شما', 'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل شما', 'class': 'form-control mb-3'}),
            'message': forms.Textarea(attrs={'placeholder': 'متن پیام شما', 'class': 'form-control mb-3', 'rows': 5}),
        }
