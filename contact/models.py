from django.db import models

# Create your models here.
class Contact(models.Model):
    title = models.CharField(max_length=50,null=False,blank=False)
    content = models.TextField(max_length=1000,null=False,blank=False)
    full_name = models.CharField(max_length=30)
    date_contact = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title