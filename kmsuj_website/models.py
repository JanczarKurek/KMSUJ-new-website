from django.db import models

class Page(models.Model):
    SITE_CHOICES = {
        ("KMSUJ", "KMS UJ"),
        ("OSSM", "OSSM")
    }
    name = models.SlugField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=100000, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    category = models.CharField(default="none", max_length=20, null=False, blank=False)
    site = models.CharField(max_length=5, default="KMSUJ", choices=SITE_CHOICES)

    def __str__(self):
        return '{} "{}"'.format(self.name, self.title)

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ("name", "site")