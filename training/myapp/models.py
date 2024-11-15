from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)  # Title of the post
    content = models.TextField()               # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp when the post was last updated

    def __str__(self):
        return self.title  # This returns the title of the post when you query it
