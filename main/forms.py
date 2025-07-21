from django import forms
from .models import Contact

class ContactForm(forms.Form):
    name= forms.CharField(max_length=100, label='نام')
    email = forms.EmailField(label='ایمیل')
    message = forms.CharField(widget=forms.Textarea, label='پیام')
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']