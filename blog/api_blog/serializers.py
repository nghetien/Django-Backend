from rest_framework import serializers
from blog.models import Blog,ImageBlog,CommentBlog,ReplyComment

class BlogPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title','body','image_cover','date_update',]

class ImageBlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageBlog
        fields = ['name_blog','image','date_change',]

class CommentBlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ['comment_blog','date_change',]

class ReplyCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = ['name_blog','reply','date_change',]