from django import forms
from .models import Blog
class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','body','image_cover']

class UpdateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','body','image_cover']

    def save(self,commit=True):
        blog = self.instance
        blog.title = self.cleaned_data['title']
        blog.body = self.cleaned_data['body']

        if self.cleaned_data['image_cover']:
            blog.image_cover=self.cleaned_data['image_cover']
        if commit:
            blog.save()
        return blog
