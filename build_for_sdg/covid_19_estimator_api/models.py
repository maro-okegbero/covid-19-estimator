from django.db import models


class Logs(models.Model):
    logs = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


