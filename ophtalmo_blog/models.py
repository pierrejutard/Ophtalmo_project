from django.db import models

# Create your models here.
class ophtalmo_article(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    image = models.ImageField(upload_to="ophtalmo_article_images",blank=True,null=True)
    text = models.TextField(blank=True)
    photo_dedication = models.CharField(max_length=128,blank=True)
    auteur = models.CharField(max_length=128)
    date = models.DateField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/ophtalmo_articles/{self.slug}/"