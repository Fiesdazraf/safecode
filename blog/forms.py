import re
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'category']  # یا هر فیلدی که داری

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        # فقط حروف انگلیسی، عدد، - و _
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise forms.ValidationError('اسلاگ (slug) باید فقط شامل حروف انگلیسی، اعداد، خط تیره (-) یا آندرلاین (_) باشد.')
        return slug
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
