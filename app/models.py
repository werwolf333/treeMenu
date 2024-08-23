from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='menu_name', default='main')
    label = models.CharField(max_length=255, verbose_name='Label')
    link = models.CharField(max_length=255, verbose_name='Link')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name='Parent'
    )

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.link.startswith('/'):
            self.link = '/' + self.link

        if not self.link.endswith('/'):
            self.link = self.link + '/'

        super().save(*args, **kwargs)
