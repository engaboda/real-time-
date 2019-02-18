from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

user = get_user_model()

class Image(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='image/')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Like(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.like)
    
    class Meta:
        unique_together = ('image','user')
    
