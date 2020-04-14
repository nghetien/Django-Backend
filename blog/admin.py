from django.contrib import admin
from blog.models import Blog,ImageBlog,CommentBlog,ReplyComment

# Register your models here.
class CommentDetail(admin.TabularInline):
    model = CommentBlog
class DetailBlog(admin.ModelAdmin):
    list_display = ['title','date_published',]
    list_filter = ['date_published','date_update']
    search_fields = ['id']
    inlines = [CommentDetail]
admin.site.register(Blog,DetailBlog)
admin.site.register(ImageBlog)
admin.site.register(CommentBlog)
admin.site.register(ReplyComment)