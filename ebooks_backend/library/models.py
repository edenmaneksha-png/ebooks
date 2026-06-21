from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Fiction',    'Fiction'),
        ('Essays',     'Essays'),
        ('Poetry',     'Poetry'),
        ('Nonfiction', 'Nonfiction'),
        ('Classics',   'Classics'),
        ('Art',        'Art & Design'),
    ]

    title        = models.CharField(max_length=512)
    author       = models.CharField(max_length=256)
    pages        = models.PositiveIntegerField(null=True, blank=True)
    category     = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default='Fiction')
    cover_url    = models.URLField(max_length=1024, blank=True)
    cover_image  = models.ImageField(upload_to='covers/', null=True, blank=True)
    description  = models.TextField(blank=True)
    pdf_file     = models.FileField(upload_to='pdfs/', null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.author}"

    def get_cover(self):
        """Returns uploaded image URL if present, else cover_url."""
        if self.cover_image:
            return self.cover_image.url
        return self.cover_url or ''


class ReadingProgress(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='progress')
    page       = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} • {self.book.title} @ p.{self.page}"
