from datetime import timedelta, datetime

from django.db import models

# Create your models here.


class URLDetail(models.Model):
    raw_body = models.TextField(null=True, blank=True)
    query_param = models.TextField(null=True, blank=True)
    headers = models.TextField()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name_plural = 'URL Detail'


class URL(models.Model):
    endpoint = models.CharField(max_length=50, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    hit_count = models.PositiveSmallIntegerField(null=False, default=0)
    url_details = models.ManyToManyField(URLDetail, blank=True)

    def __str__(self):
        return self.endpoint

    class Meta:
        verbose_name_plural = 'URL'
