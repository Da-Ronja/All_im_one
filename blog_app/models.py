from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pub_date = models.DateTimeField("date published")
    content = models.TextField()

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.content[:100] + '...'
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
