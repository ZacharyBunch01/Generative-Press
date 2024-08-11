from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('national', 'National'),
    ('international', 'International'),
    ('science_technology', 'Science & Technology'),
    ('entertainment', 'Entertainment'),
    ('business', 'Business'),
]

class Article(models.Model):
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    references = models.URLField()
    category = models.CharField(max_length=50)
    image = models.URLField(blank=True, null=True)  # Allow image to be null
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'

