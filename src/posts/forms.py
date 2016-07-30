from django import forms


from .models import BlogPost


class BlogShareForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "is_shared",
        ]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "image",
            "content",
            "draft",
            "publish",
        ]


class ContactusForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField()
    message = forms.CharField()