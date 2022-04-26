from django.db import models
from star_ratings.models import Rating

class ophtalmo_center(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    image = models.ImageField(upload_to="ophtalmo_center_images",blank=True,null=True)
    description = models.TextField(blank=True)
    marque_laser_excimer = models.CharField(max_length=128)
    date_maintenance_laser_excimer = models.DateField()
    marque_laser_femtosecond = models.CharField(max_length=128)
    date_maintenance_laser_femtosecond = models.DateField()
    lien_site_internet = models.URLField(max_length=128)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return f"/ophtalmo_centers/{self.slug}/"