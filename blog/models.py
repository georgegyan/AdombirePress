from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
tag = models.ManyToManyField(Tag, blank=True)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    class Meta:
        permissions = [
            ("can_publish_post", "Can publish post"),
            ("can_edit_all_posts", "Can edit all posts (not just own)"),
            ("can_delete_all_posts", "Can delete all posts (not just own)"),
        ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='publish_date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=255, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  # For comment moderation

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"