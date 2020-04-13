from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.

def upload_location(instance,filename,**kwargs):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id),title=str(instance.title),filename=filename,
    )
    return file_path

class Blog(models.Model):
    title = models.CharField(max_length=50,null=False,blank=False)
    body  = models.TextField(max_length=5000,null=False,blank=False)
    image_cover = models.ImageField(upload_to=upload_location,null=False,blank = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField(blank=True,unique=True)
    date_published = models.DateTimeField(auto_now_add=True,verbose_name="date published")
    date_update = models.DateTimeField(auto_now=True,verbose_name="date update")

    def __str__(self):
        return self.title

@receiver(post_delete,sender = Blog)
def submission_delete(sender,instance,**kwargs):
    instance.image_cover.delete(False)
def pre_save_blog_post_receiever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username +"-"+instance.title)
pre_save.connect(pre_save_blog_post_receiever,sender = Blog)

def upload_location_blog(instance,filename,**kwargs):
    file_path = 'image_blog/{name_blog_id}/{name_blog}-{filename}'.format(
        name_blog_id = str(instance.name_blog.id),name_blog=str(instance.name_blog),filename=filename,
    )
    return file_path

class ImageBlog(models.Model):
    name_blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    image= models.ImageField(upload_to=upload_location_blog,null=False,blank = False)