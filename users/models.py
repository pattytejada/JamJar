from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from blog.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    favorites = models.ManyToManyField(Post)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs): # resizes uploaded images to 300x300
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)