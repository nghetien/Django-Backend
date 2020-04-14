from django import forms
from .models import Blog
from blog.models import CommentBlog
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

class CommentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.author = kwargs.pop('author',None)
        self.name_blog = kwargs.pop('name_blog',None)
        super().__init__(*args,**kwargs)

    def save(self,commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.name_blog = self.name_blog
        comment.save()

    class Meta:
        model = CommentBlog
        fields = ["comment_blog",]
