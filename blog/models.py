from django.db import models
# from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# from django.contrib.auth.models import AbstractUser
from base.models import CourseCategories
from base.models import Instructors

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class BlogPost(models.Model):
    category = models.ForeignKey(CourseCategories, verbose_name="Category", default=1, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='blog_images/', blank=True, default='blog_images/defaultblog.png')
    # author_position = models.CharField(max_length=50)
    # author_bio = models.TextField(max_length=200, unique=True)
    title = models.CharField(max_length=200, unique=True, verbose_name="Title")
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Instructors, on_delete=models.CASCADE, related_name='author')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        verbose_name = "BlogPost"
        verbose_name_plural = "Posts"
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
