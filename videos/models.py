from django.db import models

class Videos(models.Model):
    title = models.CharField(max_length=100)
    alt_image = models.ImageField(upload_to='videos/alternative/images/')
    url = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_created=True,)

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name='video')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
